import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(home: const RecipePriceScreen());
  }
}

class RecipePriceScreen extends StatefulWidget {
  const RecipePriceScreen({super.key});

  @override
  State<RecipePriceScreen> createState() => _RecipePriceScreenState();
}

class _RecipePriceScreenState extends State<RecipePriceScreen> {
  String _title = "요리명 대기 중";
  String _ingredient = "재료 대기 중";
  String _price = "0";
  bool _isLoading = false;

  // 서버에서 데이터를 가져오는 함수
  Future<void> fetchPrice() async {
    setState(() {
      _isLoading = true;
    });

    try {
      // 윈도우 환경에서 실행 중인 FastAPI 주소
      final url = Uri.parse('http://127.0.0.1:8000/recipe/716429/price');
      final response = await http.get(url);

      if (response.statusCode == 200) {
        // 한글 깨짐 방지를 위해 utf8 디코딩 필수!
        final data = jsonDecode(utf8.decode(response.bodyBytes));

        setState(() {
          _title = data['recipe_title'];
          _ingredient = data['ingredient'];
          _price = data['lowest_price'];
        });
      } else {
        print("서버 에러: ${response.statusCode}");
      }
    } catch (e) {
      print("연결 에리: $e");
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("캡스톤 레시피 최저가")),
      body: Center(
        child: _isLoading
            ? const CircularProgressIndicator() // 로딩 중일 때 뺑뺑이
            : Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Text(
                    "🍳 요리: $_title",
                    style: const TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 10),
                  Text("🛒 주요 재료: $_ingredient"),
                  const SizedBox(height: 10),
                  Text(
                    "💰 최저가: $_price원",
                    style: const TextStyle(color: Colors.blue, fontSize: 18),
                  ),
                  const SizedBox(height: 30),
                  ElevatedButton(
                    onPressed: fetchPrice,
                    child: const Text("최저가 정보 가져오기"),
                  ),
                ],
              ),
      ),
    );
  }
}
