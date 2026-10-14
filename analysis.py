from clean_data import sql, energy, countries, data_2023

# --- PYTHON QUESTIONS (Q1 to Q5) ---
# Q1: Top 10 countries by renewable share, 2023

top_10=data_2023.sort_values('renewables_share_elec',ascending=False)
#print(top_10[['country','renewables_share_elec']].head(10))

# Q2: Countries above 50% renewables
morethan50=data_2023[data_2023['renewables_share_elec']>50]
#print(len(morethan50[['country','renewables_share_elec']]))
#print(morethan50[['country','renewables_share_elec']].shape)

# Q3: countries with carbon intensity of electricity above the average of all countries in 2023?
overall_avg=data_2023['carbon_intensity_elec'].mean()
#print(overall_avg)

above_avg=data_2023[data_2023['carbon_intensity_elec']>overall_avg]
#print(above_avg[['country','carbon_intensity_elec']])

# Q4: Label each country in 2023 by its fossil_share_elec
fossil_table=data_2023[['country','fossil_share_elec']].copy()
# 10 countries without fossil data were dropped
clean_fossil_table=fossil_table.dropna()
#print(clean_fossil_table)
def categoriser (fossil_share_elec):
    if fossil_share_elec >75:
        return'High'
    elif 25 <= fossil_share_elec <=75:
        return'Medium'
    else:
        return 'Low'
clean_fossil_table['Category']=clean_fossil_table['fossil_share_elec'].apply(categoriser)
#print(clean_fossil_table)
category_count= clean_fossil_table['Category'].value_counts()
#print(category_count)

#Q5: how many country names contain “Islands”, and what’s their average renewables share in 2023?
renewable_share_table=data_2023[['country','renewables_share_elec']].copy()
#print(renewable_share_table)
contains_island=renewable_share_table[renewable_share_table['country'].str.contains('Islands')]
#print(contains_island)
#print("Number of countries:",len(contains_island))
country_avg_renewable=contains_island['renewables_share_elec'].mean()
#print("Average renewables share:",country_avg_renewable)


# --- SQL QUESTIONS WITH DUCKDB (Q6 to Q10) ---

result=sql('SELECT * FROM countries')
#print(result)
# Q6: Which country had the highest solar share of electricity (solar_share_elec) each year since 2015?
q6=sql("""
      WITH ranking_table AS (
        SELECT year,country,solar_share_elec,
            RANK()OVER(PARTITION BY year ORDER BY solar_share_elec DESC) AS ranking 
        FROM countries 
        WHERE year>=2015 AND solar_share_elec IS NOT NULL
        ) 
        SELECT * FROM ranking_table WHERE ranking=1
      """)
#print(q6)

#Q7 (SQL): For each year from 2000 to 2023, how many countries had renewables_share_elec above 50%?
# Show year and count, ordered by year.

q7=sql("""
SELECT year,COUNT(country) AS no_of_countries FROM countries
WHERE renewables_share_elec>50 AND year BETWEEN 2000 AND 2023
GROUP BY year
ORDER BY year
""")
#print(q7)

#Q8 (SQL): Which countries had renewables_share_elec above 50% in every year from 2015 to 2023?
q8=sql("""
SELECT country,COUNT(year) AS no_of_years FROM countries
WHERE year BETWEEN 2015 AND 2023
AND renewables_share_elec >50
GROUP BY country
HAVING no_of_years=9
""")

#print(q8)
#print(q8.shape)

#Q9 (SQL): For each country in 2023, show its name, its solar_share_elec,
# and the world average of solar_share_elec across countries in 2023.
# Only show countries above that average.

q9=sql("""
WITH solar_share_table AS
(SELECT country,solar_share_elec,(SELECT avg(solar_share_elec) FROM countries WHERE year=2023) AS overall_avg
FROM countries
WHERE year=2023)
SELECT * FROM solar_share_table
WHERE solar_share_elec > overall_avg
""")
#print(q9)

#Q10 (SQL): For each country, show how its solar_share_elec in 2023 changed from 2022,
# as a percentage-point difference. Show the 10 countries with the biggest increase.

q10=sql("""
WITH solar_share_change AS
(SELECT country, year, solar_share_elec,
LAG(solar_share_elec) OVER(PARTITION BY country ORDER BY year) AS prev_year,
(solar_share_elec-prev_year) AS diff
FROM countries)
SELECT * FROM solar_share_change
WHERE year=2023
ORDER BY diff DESC
LIMIT 10
""")
print(q10)