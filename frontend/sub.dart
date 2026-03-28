import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false, // 오른쪽 위 디버그 띠 숨기기
      title: '자취생 요리 앱',
      theme: ThemeData(
        primarySwatch: Colors.orange, // 앱의 메인 테마 색상 (주황색)
      ),
      home: const MainScreen(),
    );
  }
}

// 값이 변하는 화면이므로 StatefulWidget을 사용합니다.
class MainScreen extends StatefulWidget {
  const MainScreen({super.key});

  @override
  State<MainScreen> createState() => _MainScreenState();
}

class _MainScreenState extends State<MainScreen> {
  // 예산 입력창의 글자를 관리하는 컨트롤러
  final TextEditingController _budgetController = TextEditingController();

  // 현재 선택된 요리 모드를 저장하는 변수
  String _selectedMode = '';

  // 요리 모드 리스트
  final List<String> _modes = ['요리 초보', '설거지 최소화', '전자레인지 전용', '10분 완성'];

  // +버튼을 눌렀을 때 예산을 더해주는 함수
  void _addBudget(int amount) {
    setState(() {
      // 현재 입력된 텍스트를 숫자로 변환 (비어있으면 0)
      int currentBudget = int.tryParse(_budgetController.text) ?? 0;
      // 금액 더하기
      int newBudget = currentBudget + amount;
      // 다시 텍스트창에 넣기
      _budgetController.text = newBudget.toString();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      // 1. 상단 바 (App Bar) 영역
      appBar: AppBar(
        backgroundColor: Colors.transparent, // 배경 투명하게
        elevation: 0, // 그림자 없애기
        // 왼쪽 상단: LV 표시
        leading: const Center(
          child: Text(
            'LV.1',
            style: TextStyle(
              color: Colors.black,
              fontWeight: FontWeight.bold,
              fontSize: 18,
            ),
          ),
        ),
        // 오른쪽 상단: 톱니바퀴 (설정) 아이콘
        actions: [
          IconButton(
            icon: const Icon(Icons.settings, color: Colors.black),
            onPressed: () {
              // 나중에 설정 화면으로 이동하는 코드 작성
              print("설정 버튼 클릭됨");
            },
          ),
        ],
      ),

      // 2. 메인 화면 내용 영역
      body: Padding(
        padding: const EdgeInsets.all(20.0), // 화면 전체에 여백 주기
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const SizedBox(height: 20), // 위쪽 여백
            // --- 중상단: 예산 입력 영역 ---
            const Text(
              '오늘의 식비 예산은\n얼마인가요? 💸',
              style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 20),

            // 직접 입력창
            TextField(
              controller: _budgetController,
              keyboardType: TextInputType.number, // 숫자 키패드만 나오게 설정
              decoration: const InputDecoration(
                labelText: '예산 직접 입력',
                suffixText: '원', // 입력창 끝에 '원' 글자 고정
                border: OutlineInputBorder(), // 네모난 테두리
              ),
            ),
            const SizedBox(height: 10),

            // 빠른 추가 버튼 (+5000, +10000)
            Row(
              children: [
                Expanded(
                  child: OutlinedButton(
                    onPressed: () => _addBudget(5000),
                    child: const Text('+ 5,000원'),
                  ),
                ),
                const SizedBox(width: 10), // 버튼 사이 간격
                Expanded(
                  child: OutlinedButton(
                    onPressed: () => _addBudget(10000),
                    child: const Text('+ 10,000원'),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 40), // 구역을 나누는 큰 여백
            // --- 중앙: 요리 모드 선택 영역 ---
            const Text(
              '원하는 요리 스타일을 선택하세요 🍳',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 15),

            // 4가지 모드 버튼 (Wrap을 사용해 바둑판처럼 자동 배치)
            Wrap(
              spacing: 10.0, // 가로 간격
              runSpacing: 10.0, // 세로 간격
              children: _modes.map((mode) {
                return ChoiceChip(
                  label: Text(mode),
                  selected: _selectedMode == mode, // 선택된 모드인지 확인
                  selectedColor: Colors.orangeAccent, // 선택되었을 때 색상
                  onSelected: (bool selected) {
                    setState(() {
                      _selectedMode = selected ? mode : ''; // 터치 시 상태 변경
                    });
                  },
                );
              }).toList(),
            ),

            const Spacer(), // 남은 공간을 밀어서 아래 버튼을 맨 밑으로 보냄
            // --- 하단: AI 추천받기 버튼 ---
            SizedBox(
              width: double.infinity, // 버튼을 가로로 꽉 차게
              height: 55, // 버튼 높이
              child: ElevatedButton(
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.orange, // 버튼 색상
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(10), // 버튼 모서리 둥글게
                  ),
                ),
                onPressed: () {
                  // 여기에 나중에 AI 추천 화면으로 넘어가는 로직 추가
                  print("입력된 예산: ${_budgetController.text}원");
                  print("선택된 모드: $_selectedMode");
                },
                child: const Text(
                  'AI 맞춤 요리 추천받기 ✨',
                  style: TextStyle(
                    fontSize: 18,
                    color: Colors.white,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
            ),
            const SizedBox(height: 20), // 맨 아래 여백
          ],
        ),
      ),
    );
  }
}
