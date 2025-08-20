---
description: Guide on how to contribute to this project
---

# How to contribute

First off, thanks for taking the time to contribute!
We use GitHub as our main collaboration platform. Please work from the `development` branch, create small feature branches, and open focused pull requests. Follow Conventional Commit messages (e.g., `feat:`, `fix:`, `docs:`), format Python code with Black, and add tests where needed. Never merge your own PR—wait for review and address all comments (including AI reviewer suggestions). Use Issues and Projects to track tasks and discussions.

> This project requires Python 3.11. Do not use Python 3.12 or newer, as it may cause dependency incompatibilities, build failure or runtime errors


## General Feedback

If you have a general feedback about our project, please do not open an issue but instead please fill in this [form](https://forms.gle/LRUq3vsFnE1QCLiA6)

## Fork & branch processing

First fork the origin repository to your own github repository, then clone the repository to your local computer.

```bash
git clone https://github.com/Your Account name/clima.git
cd clima
```

Set up the upstream repository and check the output respositories.

```bash
git remote add upstream https://github.com/CenterForTheBuiltEnvironment/clima.git

git remote -v
```

The terminal should output a list:

- `origin → your Fork repository`
- `upstream → origin repository`

Check all branches.

```bash
git branch -a
```

The terminal will show a list of branches:

```bash
> * main
  	remotes/origin/HEAD -> origin/main
  	remotes/origin/development
  	remotes/origin/main
```

Pull the development branch first, and if the terminal does not notices you that you should try the second command.

```bash
git checktout development

git checkout -b development origin/development
```

Create a new branch in the development branch.

```bash
git checkout -b (your branch name)
```

Finally update and push to your repository branch if you modify the files.

```bash
git push origin (your branch name)
```

## Pull Request Regulation
**Time to submit PR:**

- User requirements/issues have been addressed or discussed in Issue and consensus has been reached.
- Changes have been minimised (small steps/phased submission) to avoid "mega PRs".

**Classification of Common PR Types:**

- `Main (Master)`: Stable branch, merge code that passes review and CI; merge and release every time,

- `Develop`: Continuous Integration branch for daily integration with multiple collaborators.
- `Feature/*`: feature development branch, cut out from main or develop, send PR to merge in after completing the feature.
- `Fix/*`: defect repair branch, the same process as feature
- `Release/*`: release preparation branch for freezing versions, fixing documentation, doing regressions and tagging.
- `docs/*`, `chore/*`, `refactor/*`, `test/*`: documentation, miscellaneous, refactor, test type branches.
- `Style`: style modification (does not affect the function): code formatting, space adjustment, naming rules unity.
- `Refactor`: Code Refactoring: Refactor existing code to improve maintainability.
- `Test`: Add or modify tests: add unit tests, integration tests, or modify test logic.
- `Chore`: Build Configuration, Dependency Management, CI/CD Configuration Updates.
- `Perf`: Performance Optimisation: Optimising code execution efficiency or memory usage.
- `Ci`: CI Configuration Related: Changing Continuous Integration Configurations for Github Actions, Travis, Jenkins, etc.
- `Build`: build system related: modify build scripts, packaging configuration.
- `Revert`: Rollback Commit: Undoing a Previous Commit
- `Security`: Security fixes, fixing security vulnerabilities, updating dependencies to prevent attacks.
- `Deps`: Dependency Management: Dependency Management/Adding, updating, and removing dependency libraries
- `Infra`: Infrastructure related: changes to development environments, containers, server configurations, etc.

**Pull Request Strategy**
- `Constant centralization`: Added `ElementIds/ComponentProperty/ClassNames` to `components.py`. Introduce `ElementIds/ComponentProperty` for all UI IDs, replace magic strings with constants. This enables single-source-of-truth and prevents typos. No business logic changed. Verified by running callback smoke tests and snapshot tests. This is an example of modifications made in the `t_rh.py` file.

`Orginal t_rh.py file(extract)`
```python
@callback(
    Output("yearly-chart", "children"),
    [
        Input("df-store", "modified_timestamp"),
        Input("global-local-radio-input", "value"),
        Input("dropdown", "value"),
    ],
    [
        State("df-store", "data"),
        State("meta-store", "data"),
        State("si-ip-unit-store", "data"),
    ],
)
```
`Component.py: store repeated string`
```python
class ClassNames:
    CONTAINER_COL = "container-col"
    CONTAINER_COL_FULL_WIDTH = " container-col full-width"
    TEXT_NEXT_TO_INPUT = "text-next-to-input"


class ElementIds:
    DAILY = "daily"
    DF_STORE = "df-store"
    DROPDOWN = "dropdown"
    HEATMAP = "heatmap"
    GLOBAL_LOCAL_RADIO_INPUT = "global-local-radio-input"
    META_STORE = "meta-store"
    SI_IP_UNIT_STORE = "si-ip-unit-store"
    TABLE_TMP_HUM = "table-tmp-hum"
    YEARLY_CHART = "yearly-chart"


class IdButtons:
    DAILY_CHART_LABEL = "daily-chart-label"


class ComponentProperty:
    CHILDREN = "children"
    DATA = "data"
    MODIFIED_TIMESTAMP = "modified_timestamp"
    VALUE = "value"


class Text:
    DAILY_CHART = "Daily chart"
    YEARLY_CHART = "Yearly_chart"
    HEATMAP_CHART = "Heatmap chart"
    DESCRIPTIVE_STATISTICS = "Descriptive statistics"


class Type:
    CIRCLE = "circle"
```
`fixed t_rh.py(extract)`
```python
from components import ElementIds, ClassNames, Text, IdButtons, Type, ComponentProperty
@callback(
    Output(ElementIds.YEARLY_CHART, ComponentProperty.CHILDREN),
    [
        Input(ElementIds.DF_STORE, ComponentProperty.MODIFIED_TIMESTAMP),
        Input(ElementIds.GLOBAL_LOCAL_RADIO_INPUT, ComponentProperty.VALUE),
        Input(ElementIds.DROPDOWN, ComponentProperty.VALUE),
    ],
    [
        State(ElementIds.DF_STORE, ComponentProperty.DATA),
        State(ElementIds.META_STORE, ComponentProperty.DATA),
        State(ElementIds.SI_IP_UNIT_STORE, ComponentProperty.DATA),
    ],
)
```
- `Time field/timestamp harmonisation`: Unify time periods (such as hour, month) to `Colnames.hour` or `Colnames.month`. Added the `column_names.py` helper function and replaced the temporary parsing logic. Backward compatibility with old strings through a fault-tolerant parser; added round-trip testing in a multi-time zone environment. Below are three examples.

`Create a new class to fix the time field`
```python
from enum import Enum

class ColNames(str, Enum):
    """
	    DataFrame column name enumeration class, 
	    avoiding hard-coded strings
    """
    # Time-related columns
    YEAR = "year"
    MONTH = "month" 
    DAY = "day"
    HOUR = "hour"
    MINUTE = "minute"
    
    # Weather data column
    DBT = "DBT"      # dry bulb temperature
    DPT = "DPT"      # dew point temperature
    RH = "RH"        # relative humidity
    P_ATM = "p_atm"  # atmospheric pressure
    
    # Radiation-related column
    EXTR_HOR_RAD = "extr_hor_rad"      # Extraterrestrial Horizontal Radiation
    HOR_IR_RAD = "hor_ir_rad"          # Horizontal Infrared Radiation
    GLOB_HOR_RAD = "glob_hor_rad"      # Global Horizontal Radiation
    DIR_NOR_RAD = "dir_nor_rad"        # Direct Normal Radiation
    DIF_HOR_RAD = "dif_hor_rad"        # Diffuse Horizontal Radiation
    
    # Lighting-related columns
    GLOB_HOR_ILL = "glob_hor_ill"      # Global Horizontal Illuminance
    DIR_NOR_ILL = "dir_nor_ill"        # Direct Normal Illuminance
    DIF_HOR_ILL = "dif_hor_ill"        # Diffuse Horizontal Illuminance
    
    # Others
    ZLUMI = "Zlumi"                    # Luminance
    WIND_DIR = "wind_dir"              # Wind Direction
    WIND_SPEED = "wind_speed"          # Wind Speed
    TOT_SKY_COVER = "tot_sky_cover"    # Total Sky Cover
    OSKYCOVER = "Oskycover"            # Opaque Sky Cover
    VIS = "Vis"                        # Visibility
    CHEIGHT = "Cheight"                # Cloud Height
    PWobs = "PWobs"                    # Precipitation Observation
    PWcodes = "PWcodes"                # Precipitation Codes
    Pwater = "Pwater"                  # Precipitation Water
    AsolOptD = "AsolOptD"              # Aerosol Optical Depth
    SnowD = "SnowD"                    # Snow Depth
    DaySSnow = "DaySSnow"              # Daily Snow
    
    # Calculation column
    FAKE_YEAR = "fake_year"
    MONTH_NAMES = "month_names"
    UTC_TIME = "UTC_time"
    DOY = "DOY"
 ```
`Example1`
```python
# Time filtering
# Before reconstruction
def violin(df, var, global_local, si_ip):
    """Return day night violin based on the 'var' col"""
    mask_day = (df["hour"] >= 8) & (df["hour"] < 20)
    mask_night = (df["hour"] < 8) | (df["hour"] >= 20)
 
# After reconstruction   
from .column_names import ColNames

def violin(df, var, global_local, si_ip):
    """Return day night violin based on the 'var' col"""
    mask_day = (df[ColNames.HOUR] >= 8) & (df[ColNames.HOUR] < 20)
    mask_night = (df[ColNames.HOUR] < 8) | (df[ColNames.HOUR] >= 20)
```
`Example2`
```python
# DataFrame grouping operations
# Before reconstruction
def daily_profile(df, var, global_local, si_ip):
    var_month_ave = df.groupby(["month", "hour"])[var].median().reset_index()
    
    for i in range(12):
        fig.add_trace(
            go.Scatter(
                x=df.loc[df["month"] == i + 1, "hour"],
                y=df.loc[df["month"] == i + 1, var],
                # ... other props
            )
        )

# After reconstruction 
from .column_names import ColNames

def daily_profile(df, var, global_local, si_ip):
    var_month_ave = df.groupby([ColNames.MONTH, ColNames.HOUR])[var]
									    .median()
									    .reset_index()
    
    for i in range(12):
        fig.add_trace(
            go.Scatter(
                x=df.loc[df[ColNames.MONTH] == i + 1, ColNames.HOUR],
                y=df.loc[df[ColNames.MONTH] == i + 1, var],
                # ... other props
            )
        )
```

- `Progressive replacement/grey scale release`: Phase 1: Add constants; Phase 2: Batch replace references; Phase 3: Remove legacy code. The `FEATURE_USE_CONSTANT_IDS` feature switch allows for instant rollback.


## Code of Conduct

Available [here](code_of_conduct.md)

## Code style

We use Black.exe to format the code.

Install Black:

```bash
pipenv install black
```

Format your code before committing:

```bash
black .
```

## Testing

Before submitting a Pull Request, please make sure:
- All tests should pass.
- Make sure you have installed project dependencies:

```bash
npm install

pipenv install -r requirements.txt
```

From the root directory, run:

```bash
cd tests/node

npx cypress run
```

## Submitting changes

Please send a Pull Request with a clear list of what you've done. Always write a clear log message for your commits. One-line messages are fine for small changes, but bigger changes should look like this:

```text
$ git commit -m "A brief summary of the commit
> 
> A paragraph describing what changed and its impact."
```


## Thanks

Thank you again for being interested in this project! You are awesome!

