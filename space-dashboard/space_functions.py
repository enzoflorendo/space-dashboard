import pandas as pd

# convert to dashboard after using dash by plotly? (look into software)

def load_data():
    #load the space_missions.csv file and return as a DataFrame
    try:
        data = pd.read_csv("space_missions.csv")
        return data
    
    except FileNotFoundError:
        print("Error: space_missions.csv not found in the project folder.")
        return pd.DataFrame()  # <-- load empty DataFrame named pd.


# f1 - returns the total number of missions for a given company
def GetMissionCountByCompany(companyName: str) -> int:
    data = load_data()
    company_missions = data[data['Company'] == companyName]

    if company_missions.empty:
        print(f"Warning: '{companyName}' is not a valid company name.")
    
        return 0
    
    return len(company_missions)


# f2 -  calculates the success rate for a given company as a percentage
def GetSuccessRate(companyName: str) -> float:
    data = load_data()
    company_missions = data[data['Company'] == companyName]

    if company_missions.empty:
        print(f"Warning: '{companyName}' is not a valid company name.")
    
        return 0.0 

    numSuccess = ( company_missions['MissionStatus'] == "Success" ).sum()
    numTotal = len( company_missions )
    success_rate = ( numSuccess / numTotal ) * 100
    return round( success_rate, 5 )


# f3 - returns a list of all mission names launched between startDate and endDate (inclusive)
def GetMissionsByDateRange(startDate: str, endDate: str) -> list:
    data = load_data()
    data['Date'] = pd.to_datetime(data['Date'], errors = 'coerce')
    try:
        starting = pd.to_datetime(startDate)
        ending = pd.to_datetime(endDate)
    except Exception:
        print(f"Warning: inputted start date '{startDate}' or inputted end date '{endDate}' is invalid. Please try again.")
        return []

    if starting > ending:
        print(f"Warning: inputted start date '{startDate}' is after the end date '{endDate}'. Please try again.")
        return []

    missions_within_range = data[(data['Date'] >= starting) & (data['Date'] <= ending)]
    missions_within_range_list = missions_within_range.sort_values('Date')['Mission'].tolist()   
    return missions_within_range_list


# f4 - returns the top N companies ranked by total number of missions
def GetTopCompaniesByMissionCount(n: int) -> list:
    data = load_data()

    if not isinstance(n, int) or n <= 0:
        print(f"Warning: n must be a positive integer. You inputted: {n}.")
        return []

    company_mission_count = data['Company'].value_counts()

    company_mission_count = company_mission_count.sort_index(kind = 'mergesort')
    company_mission_count = company_mission_count.sort_values(ascending = False)
    top_n_companies = company_mission_count.head(n)
    top_n_companies_list = list(top_n_companies.items()) #list of tuples-ified

    return top_n_companies_list


# f5 - returns the count of missions for each mission status
def GetMissionStatusCount() -> dict:
    data = load_data()

    possible_statuses = ["Success", "Failure", "Partial Failure", "Prelaunch Failure"]

    status_count = data['MissionStatus'].value_counts()
    mission_status_count = {}

    for current_status in possible_statuses:
        mission_status_count[current_status] = int(status_count.get(current_status, 0))

    return mission_status_count


# f6 - returns the total number of missions launched in a specific year
def GetMissionsByYear(year: int) -> int:
    data = load_data()

    if not isinstance(year, int) or year < 0:
        print(f"Warning: inputted year must be a positive integer. You entered: {year}. Please try again.")
        return 0
    if year < 1957:
        print(f"Warning: The first mission launched in 1957. Please input a year that is 1957 or later. You entered: {year}. Please try again.")
        return 0

    data['Date'] = pd.to_datetime(data['Date'], errors = 'coerce')
    missions_in_year = data[data['Date'].dt.year == year]

    return len(missions_in_year)


# f7 - returns the name of the rocket that has been used the most times
def GetMostUsedRocket() -> str:
    data = load_data()
    rocket_count = data['Rocket'].value_counts()

    if rocket_count.empty:
        print("Warning: no data on rockets has been found.")
        return ""

    max_rocket_count = rocket_count.max()
    max_rocket_names = rocket_count[rocket_count == max_rocket_count].index.tolist()
    max_rocket_names.sort()
    most_used_rocket = max_rocket_names[0]
    return most_used_rocket


# f8 - calculates the average number of missions per year over a given range
def GetAverageMissionsPerYear(startYear: int, endYear: int) -> float:
    data = load_data()

    if not (isinstance(startYear, int) and isinstance(endYear, int)):
        print(f"Warning: the starting year and ending year must be integers. You inputted: {repr(startYear)} ({type(startYear).__name__}), {repr(endYear)} ({type(endYear).__name__}). Please try again.")
        return 0.0
    if startYear > endYear:
        print(f"Warning: inputted start year '{repr(startYear)}' is after the end year '{repr(endYear)}'. Please try again.")
        return 0.0
    if startYear < 1957:
        print(f"Warning: The first mission launched in 1957. Please input a year that is 1957 or later. You entered: {repr(startYear)}. Please try again.")
        return 0.0
    

    data['Date'] = pd.to_datetime(data['Date'], errors = 'coerce')

    missions_range = data[(data['Date'].dt.year >= startYear) & (data['Date'].dt.year <= endYear)]

    #avg needed - INCLUSIVE so plus one

    years_count = endYear - startYear + 1
    avg = len(missions_range) / years_count

    return round(avg, 5)

#note to enzo to double check. all functions outputting a float must round to 5 decimal places, not 2.
# --------------------------------------------- TEST CODE -------------------------------------------------
'''
# test code for f1

print (GetMissionCountByCompany("NASA"))
print (GetMissionCountByCompany("Tyler, the Creator"))
print (GetMissionCountByCompany(" "))

# test code for f2

print(GetSuccessRate("NASA"))
print(GetSuccessRate("Tyler, the Creator"))
print(GetSuccessRate(" "))

# test code for f3

print(GetMissionsByDateRange("1957-01-01", "1958-06-15"))
print(GetMissionsByDateRange("1951-01-01", "1950-01-01"))
print(GetMissionsByDateRange("NASA", "US Navy"))
print(GetMissionsByDateRange(" ", " "))

# test code for f4

print(GetTopCompaniesByMissionCount(4))
print(GetTopCompaniesByMissionCount(2.5)) #type: ignore
print(GetTopCompaniesByMissionCount(9))
print(GetTopCompaniesByMissionCount(0))
print(GetTopCompaniesByMissionCount(-1))
print(GetTopCompaniesByMissionCount("NASA")) # type: ignore
print(GetTopCompaniesByMissionCount(" ")) #type: ignore

# test code for f5

print(GetMissionStatusCount())

# test code for f6

print(GetMissionsByYear(1940))
print(GetMissionsByYear(-1957))
print(GetMissionsByYear(1957))
print(GetMissionsByYear(2000))
print(GetMissionsByYear(0))

# test code for f7

print(GetMostUsedRocket())

# test code for f8

print(GetAverageMissionsPerYear(1960, 1970))
print(GetAverageMissionsPerYear(1940, 1977))
print(GetAverageMissionsPerYear(2002, 1980))
print(GetAverageMissionsPerYear("NASA", "AMBA")) #type: ignore
print(GetAverageMissionsPerYear(0, 1))
print(GetAverageMissionsPerYear(1957, 2022))
print(GetAverageMissionsPerYear(2010, 2020))
print(GetAverageMissionsPerYear("2000", "2015")) #type: ignore
'''