"""
Census Bureau API Client

Provides a unified interface for fetching data from the U.S. Census Bureau API,
with built-in caching, error handling, and metadata tracking.

Supported APIs:
- American Community Survey (ACS) 5-year estimates
- Small Area Income and Poverty Estimates (SAIPE)
- Decennial Census

Example:
    from shared.data_fetching import CensusClient

    client = CensusClient(
        api_key='your_key_here',
        cache_dir='./cache',
        use_cache=True
    )

    # Fetch ACS data
    df = client.fetch_acs(
        year=2022,
        variables={
            'B01003_001E': 'total_population',
            'B17001_002E': 'poverty_population'
        },
        geography='county:*'
    )

    # Get metadata
    metadata = client.get_metadata()
"""

import os
import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Union

import pandas as pd
import requests


STATE_NAME_TO_FIPS = {
    "Alabama": "01", "AL": "01",
    "Alaska": "02", "AK": "02",
    "Arizona": "04", "AZ": "04",
    "Arkansas": "05", "AR": "05",
    "California": "06", "CA": "06",
    "Colorado": "08", "CO": "08",
    "Connecticut": "09", "CT": "09",
    "Delaware": "10", "DE": "10",
    "District of Columbia": "11", "DC": "11",
    "Florida": "12", "FL": "12",
    "Georgia": "13", "GA": "13",
    "Hawaii": "15", "HI": "15",
    "Idaho": "16", "ID": "16",
    "Illinois": "17", "IL": "17",
    "Indiana": "18", "IN": "18",
    "Iowa": "19", "IA": "19",
    "Kansas": "20", "KS": "20",
    "Kentucky": "21", "KY": "21",
    "Louisiana": "22", "LA": "22",
    "Maine": "23", "ME": "23",
    "Maryland": "24", "MD": "24",
    "Massachusetts": "25", "MA": "25",
    "Michigan": "26", "MI": "26",
    "Minnesota": "27", "MN": "27",
    "Mississippi": "28", "MS": "28",
    "Missouri": "29", "MO": "29",
    "Montana": "30", "MT": "30",
    "Nebraska": "31", "NE": "31",
    "Nevada": "32", "NV": "32",
    "New Hampshire": "33", "NH": "33",
    "New Jersey": "34", "NJ": "34",
    "New Mexico": "35", "NM": "35",
    "New York": "36", "NY": "36",
    "North Carolina": "37", "NC": "37",
    "North Dakota": "38", "ND": "38",
    "Ohio": "39", "OH": "39",
    "Oklahoma": "40", "OK": "40",
    "Oregon": "41", "OR": "41",
    "Pennsylvania": "42", "PA": "42",
    "Rhode Island": "44", "RI": "44",
    "South Carolina": "45", "SC": "45",
    "South Dakota": "46", "SD": "46",
    "Tennessee": "47", "TN": "47",
    "Texas": "48", "TX": "48",
    "Utah": "49", "UT": "49",
    "Vermont": "50", "VT": "50",
    "Virginia": "51", "VA": "51",
    "Washington": "53", "WA": "53",
    "West Virginia": "54", "WV": "54",
    "Wisconsin": "55", "WI": "55",
    "Wyoming": "56", "WY": "56",
    "Puerto Rico": "72", "PR": "72"
}


class CensusClient:
    """
    U.S. Census Bureau API client with caching and error handling.

    This client provides a simplified interface to Census data APIs with:
    - Automatic caching of API responses
    - Metadata tracking (sources, timestamps, record counts)
    - Error handling with graceful degradation
    - FIPS code generation for geographic identifiers
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        cache_dir: Optional[Path] = None,
        use_cache: bool = True,
        timeout: int = 30
    ):
        """
        Initialize Census API client.

        Args:
            api_key: Census API key. If None, uses CENSUS_API_KEY env var.
            cache_dir: Directory for caching API responses. Defaults to ./cache
            use_cache: Whether to use cached data when available
            timeout: Request timeout in seconds (default: 30)
        """
        self.api_key = api_key or os.getenv('CENSUS_API_KEY')
        self.use_cache = use_cache
        self.timeout = timeout

        # Set up cache directory
        if cache_dir is None:
            self.cache_dir = Path.cwd() / 'cache'
        else:
            self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True, parents=True)

        # Metadata tracking
        self.metadata = {
            'collection_date': datetime.now().isoformat(),
            'sources': {},
            'record_counts': {}
        }

    def _get_cache_path(self, cache_key: str) -> Path:
        """Generate cache file path from key."""
        # Use hash of key for filesystem safety
        key_hash = hashlib.md5(cache_key.encode()).hexdigest()
        return self.cache_dir / f"{cache_key}_{key_hash}.csv"

    def _load_from_cache(self, cache_path: Path) -> Optional[pd.DataFrame]:
        """Load DataFrame from cache if available and use_cache is True."""
        if self.use_cache and cache_path.exists():
            try:
                df = pd.read_csv(cache_path)
                return df
            except Exception as e:
                print(f"   ⚠️  Cache read error: {e}")
                return None
        return None

    def _save_to_cache(self, df: pd.DataFrame, cache_path: Path):
        """Save DataFrame to cache."""
        try:
            df.to_csv(cache_path, index=False)
        except Exception as e:
            print(f"   ⚠️  Cache write error: {e}")

    def fetch_acs(
        self,
        year: int,
        variables: Dict[str, str],
        geography: str = 'county:*',
        dataset: str = 'acs5',
        state: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Fetch data from American Community Survey (ACS).

        Args:
            year: Year of data (e.g., 2022)
            variables: Dict mapping Census variable codes to column names
                      Example: {'B01003_001E': 'total_pop', 'B17001_002E': 'poverty_pop'}
            geography: Geographic level (default: 'county:*' for all counties)
            dataset: ACS dataset (default: 'acs5' for 5-year estimates)
            state: Optional state FIPS code to limit results

        Returns:
            DataFrame with requested variables and geography
        """
        # Build cache key
        var_codes = sorted(variables.keys())
        cache_key = f"acs_{year}_{dataset}_{geography.replace(':', '_')}_{'-'.join(var_codes)}"
        if state:
            cache_key += f"_state{state}"
        cache_path = self._get_cache_path(cache_key)

        # Try cache first
        cached_df = self._load_from_cache(cache_path)
        if cached_df is not None:
            print(f"   Using cached ACS data from {cache_path.name}")
            self.metadata['sources'][cache_key] = 'cached'
            return cached_df

        # Build API request
        url = f"https://api.census.gov/data/{year}/acs/{dataset}"

        # Add NAME to get human-readable geography names
        get_vars = ['NAME'] + list(variables.keys())
        params = {
            'get': ','.join(get_vars),
            'for': geography
        }

        if state:
            params['in'] = f'state:{state}'

        if self.api_key:
            params['key'] = self.api_key

        # Make API request
        try:
            response = requests.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()

            # Convert to DataFrame
            df = pd.DataFrame(data[1:], columns=data[0])

            # Create FIPS code if geography is county
            if 'county' in geography and 'state' in df.columns and 'county' in df.columns:
                df['fips'] = df['state'] + df['county']

            # Rename variables to friendly names
            rename_map = {'NAME': 'name'}
            rename_map.update(variables)
            df = df.rename(columns=rename_map)

            # Convert numeric columns
            for orig_code, col_name in variables.items():
                if col_name in df.columns:
                    df[col_name] = pd.to_numeric(df[col_name], errors='coerce')

            # Save to cache
            self._save_to_cache(df, cache_path)

            # Update metadata
            self.metadata['sources'][cache_key] = f"Census ACS {dataset} {year}"
            self.metadata['record_counts'][cache_key] = len(df)

            print(f"   ✓ Fetched ACS data for {len(df)} geographies")
            return df

        except requests.exceptions.RequestException as e:
            print(f"   ✗ Error fetching ACS data: {e}")
            return pd.DataFrame()

    def fetch_saipe(
        self,
        year: int,
        geography: str = 'county',
        state: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Fetch Small Area Income and Poverty Estimates (SAIPE).

        Args:
            year: Year of data (e.g., 2022)
            geography: Geographic level ('county', 'state', or 'us')
            state: Optional state FIPS code to limit results

        Returns:
            DataFrame with poverty estimates
        """
        cache_key = f"saipe_{year}_{geography}"
        if state:
            cache_key += f"_state{state}"
        cache_path = self._get_cache_path(cache_key)

        # Try cache
        cached_df = self._load_from_cache(cache_path)
        if cached_df is not None:
            print(f"   Using cached SAIPE data from {cache_path.name}")
            self.metadata['sources'][cache_key] = 'cached'
            return cached_df

        # Build API request
        url = f"https://api.census.gov/data/{year}/acs/acs5"

        # SAIPE variables
        variables = {
            'B17001_001E': 'total_pop',
            'B17001_002E': 'poverty_pop'
        }

        params = {
            'get': f"NAME,{','.join(variables.keys())}",
            'for': f'{geography}:*'
        }

        if state and geography == 'county':
            params['in'] = f'state:{state}'

        if self.api_key:
            params['key'] = self.api_key

        try:
            response = requests.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()

            df = pd.DataFrame(data[1:], columns=data[0])

            # Create FIPS for counties
            if geography == 'county' and 'state' in df.columns and 'county' in df.columns:
                df['fips'] = df['state'] + df['county']

            df = df.rename(columns={
                'NAME': 'name',
                **variables
            })

            # Convert numeric
            df['total_pop'] = pd.to_numeric(df['total_pop'], errors='coerce')
            df['poverty_pop'] = pd.to_numeric(df['poverty_pop'], errors='coerce')

            # Calculate poverty rate
            df['poverty_rate'] = (df['poverty_pop'] / df['total_pop'] * 100).round(2)

            self._save_to_cache(df, cache_path)

            self.metadata['sources'][cache_key] = f"Census ACS {year} (SAIPE proxy)"
            self.metadata['record_counts'][cache_key] = len(df)

            print(f"   ✓ Fetched SAIPE data for {len(df)} geographies")
            return df

        except requests.exceptions.RequestException as e:
            print(f"   ✗ Error fetching SAIPE data: {e}")
            return pd.DataFrame()

    def fetch_population(
        self,
        year: int,
        geography: str = 'county:*',
        state: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Fetch total population counts.

        Args:
            year: Year of data
            geography: Geographic level
            state: Optional state FIPS code

        Returns:
            DataFrame with population data
        """
        return self.fetch_acs(
            year=year,
            variables={'B01003_001E': 'total_population'},
            geography=geography,
            state=state
        )

    def get_county_fips(self, state_name: str, county_name: str) -> Optional[str]:
        """
        Look up FIPS code for a county.

        Note: This requires a pre-loaded FIPS code table. For now, returns None.
        Future enhancement: Load from Census geocoding API.

        Args:
            state_name: State name (e.g., "California")
            county_name: County name (e.g., "Los Angeles")

        Returns:
            5-digit FIPS code or None
        """
        if not state_name or not county_name:
            return None
            
        # Get state FIPS
        state_fips = self.get_state_fips(state_name)
        if not state_fips:
            print(f"   ⚠️  Could not find FIPS for state: {state_name}")
            return None
            
        # Check cache/metadata for counties in this state
        cache_key = f"counties_list_{state_fips}"
        cache_path = self._get_cache_path(cache_key)
        
        # Load county list (either from cache or fetch new)
        counties_df = self._load_from_cache(cache_path)
        
        if counties_df is None:
            # Fetch from API
            print(f"   Fetching county list for {state_name} ({state_fips})...")
            try:
                # Use 2020 Decennial or latest ACS as source for county names
                url = "https://api.census.gov/data/2020/dec/pl" 
                params = {
                    'get': 'NAME',
                    'for': 'county:*',
                    'in': f'state:{state_fips}'
                }
                if self.api_key:
                    params['key'] = self.api_key
                    
                response = requests.get(url, params=params, timeout=self.timeout)
                response.raise_for_status()
                data = response.json()
                
                counties_df = pd.DataFrame(data[1:], columns=data[0])
                self._save_to_cache(counties_df, cache_path)
                
            except requests.exceptions.RequestException as e:
                # Fallback to ACS if decennial fails
                try:
                    url = "https://api.census.gov/data/2022/acs/acs5"
                    params = {
                        'get': 'NAME',
                        'for': 'county:*',
                        'in': f'state:{state_fips}'
                    }
                    if self.api_key:
                        params['key'] = self.api_key
                    
                    response = requests.get(url, params=params, timeout=self.timeout)
                    response.raise_for_status()
                    data = response.json()
                    
                    counties_df = pd.DataFrame(data[1:], columns=data[0])
                    self._save_to_cache(counties_df, cache_path)
                except Exception as e2:
                    print(f"   ✗ Error fetching county list: {e2}")
                    return None
        
        # Search for county
        # Normalize search: "Travis" -> match "Travis County"
        target_name = county_name.lower()
        if "county" not in target_name and "parish" not in target_name:
             target_name_simple = target_name
        else:
             target_name_simple = target_name.replace(" county", "").replace(" parish", "")

        for _, row in counties_df.iterrows():
            fips_full = row['state'] + row['county']
            name_full = row['NAME'].lower() # e.g. "Autauga County, Alabama"
            name_part = name_full.split(',')[0] # "autauga county"
            
            # Exact match on full name
            if target_name in name_part:
                return fips_full
                
            # Match without "County" suffix matching
            if target_name_simple == name_part.replace(" county", "").replace(" parish", ""):
                return fips_full

        print(f"   ⚠️  County '{county_name}' not found in {state_name}")
        return None

    def get_state_fips(self, state_name_or_abbr: str) -> Optional[str]:
        """
        Get 2-digit FIPS code for a state name or abbreviation.
        
        Args:
            state_name_or_abbr: Full name (California) or Abbr (CA)
            
        Returns:
            2-digit FIPS string or None
        """
        if not state_name_or_abbr:
            return None
            
        key = state_name_or_abbr.strip()
        # Try direct match (case sensitive first)
        if key in STATE_NAME_TO_FIPS:
            return STATE_NAME_TO_FIPS[key]
            
        # Try case insensitive
        # Build reverse map for case insensitivity if needed, but simple iteration is fine for 50 states
        for name, fips in STATE_NAME_TO_FIPS.items():
            if name.lower() == key.lower():
                return fips
                
        return None

    def generate_metadata(self, source: str, dataset: str) -> Dict:
        """
        Generate metadata dictionary for a dataset.

        Args:
            source: Data source name (e.g., "Census Bureau")
            dataset: Dataset name (e.g., "ACS 2022")

        Returns:
            Dict with metadata
        """
        return {
            'source': source,
            'dataset': dataset,
            'collection_date': datetime.now().isoformat(),
            'api_key_used': bool(self.api_key),
            'cache_enabled': self.use_cache,
            'cache_directory': str(self.cache_dir)
        }

    def get_metadata(self) -> Dict:
        """
        Get metadata for all fetches performed by this client instance.

        Returns:
            Dict with collection metadata
        """
        return self.metadata

    def save_metadata(self, filepath: Union[str, Path]):
        """
        Save metadata to JSON file.

        Args:
            filepath: Path to save metadata JSON
        """
        filepath = Path(filepath)
        with open(filepath, 'w') as f:
            json.dump(self.metadata, f, indent=2)
        print(f"   ✓ Metadata saved to {filepath}")

    def clear_cache(self, pattern: Optional[str] = None):
        """
        Clear cached files.

        Args:
            pattern: Optional glob pattern to match specific files (e.g., "acs_2022*")
                    If None, clears all cache files.
        """
        if pattern:
            files = list(self.cache_dir.glob(f"{pattern}"))
        else:
            files = list(self.cache_dir.glob("*.csv"))

        count = 0
        for file in files:
            try:
                file.unlink()
                count += 1
            except Exception as e:
                print(f"   ⚠️  Error deleting {file}: {e}")

        print(f"   ✓ Cleared {count} cached file(s)")


# Convenience function for quick access
def create_census_client(
    api_key: Optional[str] = None,
    cache_dir: Optional[Path] = None,
    use_cache: bool = True
) -> CensusClient:
    """
    Create a CensusClient with sensible defaults.

    Args:
        api_key: Census API key (uses CENSUS_API_KEY env var if None)
        cache_dir: Cache directory (defaults to ./cache)
        use_cache: Whether to use caching

    Returns:
        Configured CensusClient instance
    """
    return CensusClient(api_key=api_key, cache_dir=cache_dir, use_cache=use_cache)
