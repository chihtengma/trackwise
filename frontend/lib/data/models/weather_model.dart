import 'package:json_annotation/json_annotation.dart';

part 'weather_model.g.dart';

@JsonSerializable()
class WeatherCurrentResponse {
  final String location;
  @JsonKey(name: 'temp_celsius')
  final double tempCelsius;
  @JsonKey(name: 'temp_fahrenheit')
  final double tempFahrenheit;
  @JsonKey(name: 'feels_like_celsius')
  final double feelsLikeCelsius;
  final String condition;
  final String description;
  final int humidity;
  @JsonKey(name: 'wind_speed')
  final double windSpeed;
  @JsonKey(name: 'visibility_km')
  final double visibilityKm;

  WeatherCurrentResponse({
    required this.location,
    required this.tempCelsius,
    required this.tempFahrenheit,
    required this.feelsLikeCelsius,
    required this.condition,
    required this.description,
    required this.humidity,
    required this.windSpeed,
    required this.visibilityKm,
  });

  factory WeatherCurrentResponse.fromJson(Map<String, dynamic> json) =>
      _$WeatherCurrentResponseFromJson(json);

  Map<String, dynamic> toJson() => _$WeatherCurrentResponseToJson(this);
}

@JsonSerializable()
class WeatherQuery {
  final String location;

  WeatherQuery({required this.location});

  factory WeatherQuery.fromJson(Map<String, dynamic> json) =>
      _$WeatherQueryFromJson(json);

  Map<String, dynamic> toJson() => _$WeatherQueryToJson(this);
}
