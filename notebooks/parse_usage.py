import pandas as pd

YEARS = {
    2022: {'file': 'files/2022.xlsx', 'month_count': 12},
    2023: {'file': 'files/2023.xlsx', 'month_count': 12},
    2024: {'file': 'files/2024.xlsx', 'month_count': 5},
}

all_budgets = []
RESULTS = {}

for year, params in YEARS.items():

    df = pd.read_excel(params['file'], index_col=0, header=0)

    df = df[df['Product'].str.startswith('research-cloud', na=False)]
    cpu = df[df['SrvUnit'] == 'cpu-hr']
    gpu = df[df['SrvUnit'] == 'gpu-hr']

    RESULTS[year] = {}
    months = {}

    for i in range(1,params['month_count']+1):
        months[i] = {}
        months[i]['cpu'] = cpu["{:d}-{:02d}".format(year, i)].sum()
        months[i]['gpu'] = gpu["{:d}-{:02d}".format(year, i)].sum()
        months[i]['total'] = months[i]['gpu'] + months[i]['cpu']
        RESULTS[year]['total_usage'] = RESULTS[year].get('total_usage', 0) + months[i]['total']

    RESULTS[year]['monthly_usage'] = months

    budgets = set(df.index.values)
    all_budgets.extend(list(budgets))
    RESULTS[year]['active_budgets'] = len(budgets)

print(RESULTS)