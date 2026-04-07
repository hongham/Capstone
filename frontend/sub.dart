import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: '자취생 요리 앱',
      theme: ThemeData(
        primarySwatch: Colors.orange,
        scaffoldBackgroundColor: Colors.grey[50], // 전체 배경색 약간 밝은 회색
      ),
      home: const MainScreen(),
    );
  }
}

// ==========================================
// 1. 메인 화면 (예산 및 모드 선택) - 기존 코드 유지/수정
// ==========================================
class MainScreen extends StatefulWidget {
  const MainScreen({super.key});

  @override
  State<MainScreen> createState() => _MainScreenState();
}

class _MainScreenState extends State<MainScreen> {
  final TextEditingController _budgetController = TextEditingController();
  String _selectedMode = '';
  final List<String> _modes = ['요리 초보', '설거지 최소화', '전자레인지 전용', '10분 완성'];

  void _addBudget(int amount) {
    setState(() {
      int currentBudget = int.tryParse(_budgetController.text) ?? 0;
      _budgetController.text = (currentBudget + amount).toString();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0,
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
        actions: [
          IconButton(
            icon: const Icon(Icons.settings, color: Colors.black),
            onPressed: () {},
          ),
        ],
      ),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const SizedBox(height: 20),
            const Text(
              '오늘의 식비 예산은\n얼마인가요? 💸',
              style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 20),
            TextField(
              controller: _budgetController,
              keyboardType: TextInputType.number,
              decoration: const InputDecoration(
                labelText: '예산 직접 입력',
                suffixText: '원',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 10),
            Row(
              children: [
                Expanded(
                  child: OutlinedButton(
                    onPressed: () => _addBudget(5000),
                    child: const Text('+ 5,000원'),
                  ),
                ),
                const SizedBox(width: 10),
                Expanded(
                  child: OutlinedButton(
                    onPressed: () => _addBudget(10000),
                    child: const Text('+ 10,000원'),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 40),
            const Text(
              '원하는 요리 스타일을 선택하세요 🍳',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 15),
            Wrap(
              spacing: 10.0,
              runSpacing: 10.0,
              children: _modes.map((mode) {
                return ChoiceChip(
                  label: Text(mode),
                  selected: _selectedMode == mode,
                  selectedColor: Colors.orange[200],
                  onSelected: (bool selected) {
                    setState(() {
                      _selectedMode = selected ? mode : '';
                    });
                  },
                );
              }).toList(),
            ),
            const Spacer(),
            SizedBox(
              width: double.infinity,
              height: 55,
              child: ElevatedButton(
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.orange,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(10),
                  ),
                ),
                onPressed: () {
                  if (_budgetController.text.isEmpty || _selectedMode.isEmpty) {
                    ScaffoldMessenger.of(context).showSnackBar(
                      const SnackBar(content: Text('예산과 모드를 모두 선택해주세요!')),
                    );
                    return;
                  }
                  // 다음 화면(레시피 추천 리스트)으로 이동
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (context) => RecipeListScreen(
                        budget: int.parse(_budgetController.text),
                        mode: _selectedMode,
                      ),
                    ),
                  );
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
            const SizedBox(height: 20),
          ],
        ),
      ),
    );
  }
}

// ==========================================
// 2. 추천 요리 리스트 출력 화면 (AI 추천 결과)
// ==========================================
class RecipeListScreen extends StatelessWidget {
  final int budget;
  final String mode;

  const RecipeListScreen({super.key, required this.budget, required this.mode});

  @override
  Widget build(BuildContext context) {
    // 가상의 AI 추천 데이터 (플로우차트: 추천 요리 리스트 출력)
    final mockRecipes = [
      {
        'name': '원팬 돼지고기 숙주볶음',
        'cost': 7500,
        'time': '15분',
        'tag': '#가성비최고 #설거지1개',
      },
      {'name': '전자레인지 계란치즈밥', 'cost': 3000, 'time': '5분', 'tag': '#초간단 #전자레인지'},
      {'name': '참치마요 덮밥', 'cost': 4500, 'time': '10분', 'tag': '#불안씀 #단백질'},
    ];

    return Scaffold(
      appBar: AppBar(
        title: const Text('AI 추천 레시피', style: TextStyle(color: Colors.black)),
        backgroundColor: Colors.white,
        iconTheme: const IconThemeData(color: Colors.black),
        elevation: 1,
      ),
      body: ListView.builder(
        padding: const EdgeInsets.all(16),
        itemCount: mockRecipes.length,
        itemBuilder: (context, index) {
          final recipe = mockRecipes[index];
          return Card(
            margin: const EdgeInsets.only(bottom: 16),
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(12),
            ),
            child: ListTile(
              contentPadding: const EdgeInsets.all(16),
              title: Text(
                recipe['name'] as String,
                style: const TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                ),
              ),
              subtitle: Padding(
                padding: const EdgeInsets.only(top: 8.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      recipe['tag'] as String,
                      style: TextStyle(color: Colors.orange[700]),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      '예상 비용: ${recipe['cost']}원 / 예상 시간: ${recipe['time']}',
                    ),
                  ],
                ),
              ),
              trailing: const Icon(Icons.arrow_forward_ios, size: 16),
              onTap: () {
                // 플로우차트: '요리 선택' -> AI 장바구니 최적화 화면으로 이동
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => RecipeDetailScreen(
                      recipeName: recipe['name'] as String,
                    ),
                  ),
                );
              },
            ),
          );
        },
      ),
    );
  }
}

// ==========================================
// 3. AI 장바구니 최적화 & 요리 상세 화면
// ==========================================
class RecipeDetailScreen extends StatelessWidget {
  final String recipeName;

  const RecipeDetailScreen({super.key, required this.recipeName});

  // 플로우차트 마지막 '요리 시작 및 완료 -> 경험치 획득' 팝업 띄우기
  void _finishCooking(BuildContext context) {
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (context) {
        return AlertDialog(
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(16),
          ),
          title: const Text('🎉 요리 완성!', textAlign: TextAlign.center),
          content: const Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Text('맛있는 식사 하세요!'),
              SizedBox(height: 10),
              Text(
                '경험치 +50 XP 획득',
                style: TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                  color: Colors.orange,
                ),
              ),
              Text('레벨 2까지 30XP 남았습니다.'),
            ],
          ),
          actions: [
            Center(
              child: ElevatedButton(
                style: ElevatedButton.styleFrom(backgroundColor: Colors.orange),
                onPressed: () {
                  // 다이얼로그 닫고 메인화면으로 복귀 (스택 비우기)
                  Navigator.of(context).popUntil((route) => route.isFirst);
                },
                child: const Text(
                  '메인으로 돌아가기',
                  style: TextStyle(color: Colors.white),
                ),
              ),
            ),
          ],
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(recipeName, style: const TextStyle(color: Colors.black)),
        backgroundColor: Colors.white,
        iconTheme: const IconThemeData(color: Colors.black),
        elevation: 1,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // 섹션 1: AI 최적화 장바구니 (시퀀스 다이어그램 Gemini AI 산출물 반영)
            const Text(
              '🛒 AI 장바구니 최적화 (가성비 비교)',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 10),
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    _buildCartItem('돼지고기(앞다리살)', '소용량 300g (단가 저렴)', '4,500원'),
                    _buildCartItem('숙주나물', '대용량 500g (가성비 추천)', '1,200원'),
                    _buildCartItem('대파', '1단 (유통기한 김)', '1,800원'),
                    const Divider(),
                    const Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Text(
                          '총 예상 구매 금액',
                          style: TextStyle(fontWeight: FontWeight.bold),
                        ),
                        Text(
                          '7,500원',
                          style: TextStyle(
                            fontWeight: FontWeight.bold,
                            color: Colors.orange,
                            fontSize: 18,
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 30),

            // 섹션 2: 남은 재료 활용법 (다이어그램 반영)
            const Text(
              '💡 남은 재료 AI 활용법',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 10),
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: Colors.blue[50],
                borderRadius: BorderRadius.circular(10),
              ),
              child: const Text(
                '숙주나물이 300g 정도 남을 예정입니다.\n내일 아침 "숙주 라면"이나 "숙주 계란말이"를 해드시는 것을 추천해요!',
                style: TextStyle(fontSize: 15, height: 1.4),
              ),
            ),
            const SizedBox(height: 30),

            // 섹션 3: 레시피 순서 (간단히 표시)
            const Text(
              '🍳 조리 순서',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 10),
            const Text(
              '1. 프라이팬에 식용유를 두르고 대파를 볶아 파기름을 냅니다.\n2. 돼지고기를 넣고 볶아줍니다.\n3. 고기가 익으면 숙주를 넣고 굴소스로 간을 하여 강불에 빠르게 볶습니다.',
              style: TextStyle(fontSize: 16, height: 1.5),
            ),
            const SizedBox(height: 40),
          ],
        ),
      ),
      // 하단 고정 버튼 (요리 완료)
      bottomNavigationBar: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(20.0),
          child: SizedBox(
            height: 55,
            child: ElevatedButton(
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.orange,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(10),
                ),
              ),
              onPressed: () => _finishCooking(context),
              child: const Text(
                '요리 완료! (경험치 받기) 🏆',
                style: TextStyle(
                  fontSize: 18,
                  color: Colors.white,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }

  // 장바구니 아이템 UI 헬퍼 위젯
  Widget _buildCartItem(String name, String desc, String price) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 12.0),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  name,
                  style: const TextStyle(
                    fontWeight: FontWeight.bold,
                    fontSize: 16,
                  ),
                ),
                Text(
                  desc,
                  style: const TextStyle(color: Colors.grey, fontSize: 12),
                ),
              ],
            ),
          ),
          Text(price, style: const TextStyle(fontSize: 16)),
        ],
      ),
    );
  }
}
