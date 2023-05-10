/*
import 'package:flutter/services.dart' show rootBundle;
import 'package:tuple/tuple.dart';
import 'package:excel/excel.dart';
import 'package:interpolation/interpolation.dart' as interp;

Future<double> calculatePercentileFromTable(
    String tableFilePath,
    String tabPath,
    int targetAgeInDays,
    List<double> percentileValues,
    double targetMeasureValue) async {
  // read the Excel file and extract the age in days from the first column of each row
  final bytes = await rootBundle.load(tableFilePath);
  final excel = Excel.decodeBytes(bytes.buffer.asUint8List());
  final sheet = excel.tables[tabPath];
  final ages = sheet.columns[0].cells.map((cell) => cell.value as int).toList();

  // read the percentiles and measure values for the row corresponding to the target age
  final row = sheet.rows.firstWhere((row) => row[0].value == targetAgeInDays);
  final percentilesAndMeasures =
      row.sublist(1).map((cell) => cell.value as double).toList();

  // extract the percentiles and measure values
  final percentiles = percentileValues;
  final measures = percentilesAndMeasures;

  // perform cubic spline interpolation on the percentiles and measure values
  final interpolation = interp.CubicSpline(x: percentiles, y: measures);

  // find the percentile value corresponding to the target measure value using inverse interpolation
  final inverseInterpolation = interpolation.inverse(targetMeasureValue);
  final percentile = inverseInterpolation.item2;

  return percentile;
}

*/
