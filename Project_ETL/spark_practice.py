# Databricks notebook source
path = "/Volumes/workspace/neon_db/de_prectice/weather_clean.csv"
df = spark.read.csv(path, header=True, inferSchema=True)
df.printSchema()
df.count()

# COMMAND ----------

from pyspark.sql import functions as F
from pyspark.sql.window import Window

# # Task 2: Compute overall average temperature and filter rows above it
# avg_temp = df.agg(F.avg("temperature_c")).first()[0]
# print(f"Overall Average Temperature: {avg_temp:.2f}°C")

# filtered_df = df.filter(F.col("temperature_c") > avg_temp)
# row_count = filtered_df.count()
# print(f"Row count after filter: {row_count}")

# # Task 3: Add temp_f column and show a sample
# df_with_f = filtered_df.withColumn("temp_f", F.col("temperature_c") * 9 / 5 + 32)
# df_with_f.select("observed_at", "temperature_c", "temp_f").show(5, truncate=False)



# result = (
#     df.groupBy("obs_date")
#       .agg(
#           F.avg("temperature_c").alias("avg_temp"),
#           F.avg("humidity_pct").alias("avg_humidity"),
#       )
#       .orderBy("obs_date")
# )
# result.show()


# w = Window.partitionBy("obs_date").orderBy(F.col("temperature_c").desc())

# hottest = (
#     df.withColumn("rnk", F.dense_rank().over(w))
#       .filter(F.col("rnk") == 1)
#       .select("obs_date", "observed_at", "temperature_c", "rnk")
#       .orderBy("obs_date")
# )
# hottest.show()


out_path = "/Volumes/workspace/neon_db/de_prectice/hottest_per_day"

hottest.write.mode("overwrite").parquet(out_path)

check = spark.read.parquet(out_path)
print(check.count())
check.printSchema()