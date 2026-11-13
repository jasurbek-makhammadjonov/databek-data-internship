from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, lag, unix_timestamp, when,
    sum as spark_sum, to_date,
    min as spark_min, max as spark_max,
    countDistinct, avg
)
from pyspark.sql.window import Window

spark = SparkSession.builder.appName("ClickstreamSessionization").getOrCreate()

# Sample data
data = [
    ("u1", "2024-01-01 10:00:00", "/home"),
    ("u1", "2024-01-01 10:10:00", "/products"),
    ("u1", "2024-01-01 11:00:00", "/cart"),
    ("u2", "2024-01-01 09:00:00", "/home"),
    ("u2", "2024-01-01 09:20:00", "/search"),
    ("u2", "2024-01-01 10:00:00", "/checkout"),
]

df = spark.createDataFrame(data, ["user_id", "ts", "url"])

# Window per user
w = Window.partitionBy("user_id").orderBy("ts")

# Previous timestamp
df2 = df.withColumn("prev_ts", lag("ts").over(w))

# Time difference in minutes
df2 = df2.withColumn(
    "gap_minutes",
    (
        unix_timestamp("ts") -
        unix_timestamp("prev_ts")
    ) / 60
)

# New session if inactivity > 30 min
df2 = df2.withColumn(
    "new_session",
    when(
        (col("prev_ts").isNull()) |
        (col("gap_minutes") > 30),
        1
    ).otherwise(0)
)

# Session number per user
df2 = df2.withColumn(
    "session_id",
    spark_sum("new_session").over(
        w.rowsBetween(Window.unboundedPreceding, 0)
    )
)

print("Sessionized Events")
df2.show(truncate=False)

# Session metrics
sessions = (
    df2.groupBy("user_id", "session_id")
       .agg(
           spark_min("ts").alias("session_start"),
           spark_max("ts").alias("session_end")
       )
)

sessions = sessions.withColumn(
    "session_length_minutes",
    (
        unix_timestamp("session_end")
        - unix_timestamp("session_start")
    ) / 60
)

sessions = sessions.withColumn(
    "session_day",
    to_date("session_start")
)

# Sessions per day
sessions_per_day = (
    sessions.groupBy("session_day")
            .agg(
                countDistinct("session_id").alias("sessions_count")
            )
)

print("Sessions Per Day")
sessions_per_day.show()

# Average session length
avg_session_length = (
    sessions.agg(
        avg("session_length_minutes")
        .alias("avg_session_length_minutes")
    )
)

print("Average Session Length")
avg_session_length.show()

spark.stop()