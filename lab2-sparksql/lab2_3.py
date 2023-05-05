from pyspark import SparkContext
from pyspark.sql import SQLContext, Row
from pyspark.sql import functions as F

sc = SparkContext(appName = "Lab2")
sqlContext = SQLContext(sc)

#Loading text file and convert each line to a Row
temperature_file = sc.textFile("BDA/input/temperature-readings.csv")
lines = temperature_file.map(lambda line: line.split(";"))

tempReadings = lines.map(lambda p: Row(station=p[0], date=p[1], year=int(p[1].split("-")[0]),month = int(p[1].split("-")[1]), time=p[2], temp=float(p[3]), quality=p[4]))

schemaTempReadings = sqlContext.createDataFrame(tempReadings)

schemaTempReadings.registerTempTable("tempReadings")

tmp_schema = schemaTempReadings.filter( (schemaTempReadings['year'] >= 1960) & (schemaTempReadings['year'] <= 2014))

lab2_3 = tmp_schema.groupBy(tmp_schema['year'],tmp_schema['month'],tmp_schema['station']).agg(F.avg(tmp_schema['temp']).alias('avgtemp'))
lab2_3 = lab2_3.orderBy(lab2_3['avgtemp'],ascending=False)
print("ABCDE")
lab2_3.show()
last = lab2_3.rdd
last.saveAsTextFile("BDA/output")
