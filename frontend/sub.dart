import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

void main() {
  runApp(
    MultiProvider(
      providers: [ChangeNotifierProvider(create: (_) => RecipeProvider())],
      child: const MyApp(),
    ),
  );
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Recipe App Skeleton',
      theme: ThemeData(
        primarySwatch: Colors.grey,
        scaffoldBackgroundColor: Colors.white,
      ),
      home: const HomeScreen(), // 1번 화면
    );
  }
}

// ==========================================
// 1. Models (API 요청/응답 형태 정의)
// ==========================================
class Recipe {
  final String id;
  final String title;
  final String imageUrl;
  final String description;

  Recipe({
    required this.id,
    required this.title,
    required this.imageUrl,
    required this.description,
  });
}

class RecipeRequest {
  String? cuisine;
  int? budget;
  String? difficulty;
  String? ingredients;

  // 나중에 API Request Body로 변환할 메서드
  Map<String, dynamic> toJson() => {
    'cuisine': cuisine,
    'budget': budget,
    'difficulty': difficulty,
    'ingredients': ingredients,
  };
}

// ==========================================
// 2. Services (가짜 데이터 & API 스위치 역할)
// 나중에 여기서 Future.delayed를 http.get/post로만 바꾸면 됩니다.
// ==========================================
class ApiService {
  // 요리 추천 검색 API (Mock)
  static Future<List<Recipe>> fetchRecipes(RecipeRequest request) async {
    await Future.delayed(const Duration(seconds: 2)); // API 통신 로딩 대기 상태 시뮬레이션

    // 1-4-1 분기점 오류 메세지 시뮬레이션 (예: 예산이 1000원 미만일 경우 예외 발생)
    if (request.budget != null && request.budget! < 1000) {
      throw Exception('금액에 맞는 요리를 찾을 수 없습니다.');
    }

    // 정상 결과 가짜 데이터 반환
    return [
      Recipe(
        id: '1',
        title: '김치찌개',
        imageUrl: '',
        description: '김치찌개 레시피 내용\n~~~~~~~~~~~~~~~~~~~~~',
      ),
      Recipe(
        id: '2',
        title: '된장찌개',
        imageUrl: '',
        description: '된장찌개 레시피 내용\n~~~~~~~~~~~~~~~~~~~~~',
      ),
    ];
  }

  // 레시피함 목록 API (Mock)
  static Future<List<Recipe>> fetchSavedRecipes(String query) async {
    await Future.delayed(const Duration(seconds: 1));
    return [
      Recipe(
        id: '3',
        title: '저장된 제육볶음',
        imageUrl: '',
        description: '저장된 레시피 내용',
      ),
      Recipe(
        id: '4',
        title: '저장된 파스타',
        imageUrl: '',
        description: '저장된 레시피 내용',
      ),
    ];
  }
}

// ==========================================
// 3. State Management (상태 관리 및 비즈니스 로직)
// ==========================================
class RecipeProvider with ChangeNotifier {
  RecipeRequest currentRequest = RecipeRequest();

  bool isLoading = false;
  String? errorMessage;
  List<Recipe> recommendedRecipes = [];
  List<Recipe> savedRecipes = [];

  void setCuisine(String cuisine) {
    currentRequest.cuisine = cuisine;
    notifyListeners();
  }

  void setBudget(int budget) {
    currentRequest.budget = budget;
    notifyListeners();
  }

  void setDifficulty(String diff) {
    currentRequest.difficulty = diff;
    notifyListeners();
  }

  void setIngredients(String ingredients) {
    currentRequest.ingredients = ingredients;
    notifyListeners();
  }

  // API 호출 및 상태 변경 (Loading -> Data or Error)
  Future<bool> submitSearch() async {
    isLoading = true;
    errorMessage = null;
    notifyListeners();

    try {
      recommendedRecipes = await ApiService.fetchRecipes(currentRequest);
      isLoading = false;
      notifyListeners();
      return true; // 성공
    } catch (e) {
      isLoading = false;
      errorMessage = e.toString().replaceAll('Exception: ', '');
      notifyListeners();
      return false; // 실패
    }
  }

  Future<void> loadSavedRecipes(String query) async {
    isLoading = true;
    notifyListeners();
    savedRecipes = await ApiService.fetchSavedRecipes(query);
    isLoading = false;
    notifyListeners();
  }

  void resetFlow() {
    currentRequest = RecipeRequest();
    recommendedRecipes = [];
    errorMessage = null;
    notifyListeners();
  }
}

// ==========================================
// 4. Screens (화면 UI 흐름)
// ==========================================

// 공통 UI 컴포넌트 (버튼)
class GreyButton extends StatelessWidget {
  final String text;
  final VoidCallback onPressed;
  final bool isSelected;

  const GreyButton({
    Key? key,
    required this.text,
    required this.onPressed,
    this.isSelected = false,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onPressed, // [수정됨] onPressed -> onTap
      child: Container(
        padding: const EdgeInsets.symmetric(vertical: 15),
        margin: const EdgeInsets.only(bottom: 10),
        width: double.infinity,
        color: isSelected ? Colors.grey[500] : Colors.grey[300],
        child: Center(child: Text(text)),
      ),
    );
  }
}

// --- 1번 화면: 홈 ---
class HomeScreen extends StatelessWidget {
  const HomeScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('1번 화면')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Text('1.레시피찾기,레시피함'),
            const SizedBox(height: 50),
            GreyButton(
              text: '레시피찾기',
              onPressed: () {
                context.read<RecipeProvider>().resetFlow();
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (_) => const CuisineScreen()),
                );
              },
            ),
            const SizedBox(height: 20),
            GestureDetector(
              onTap: () {
                // [수정됨] onPressed -> onTap
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (_) => const RecipeBoxScreen()),
                );
              },
              child: Container(
                padding: const EdgeInsets.all(20),
                color: Colors.red[300],
                child: const Text('레시피\n피함', textAlign: TextAlign.center),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

// --- 1-1번 화면: 요리종류선택 ---
class CuisineScreen extends StatelessWidget {
  const CuisineScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final provider = context.watch<RecipeProvider>();
    final cuisines = ['한식', '양식', '중식', '일식', '디저트', '아무거나(기타)'];

    return Scaffold(
      appBar: AppBar(title: const Text('1-1번화면 요리종류선택')),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          children: [
            ...cuisines.map(
              (c) => GreyButton(
                text: c,
                isSelected: provider.currentRequest.cuisine == c,
                onPressed: () => provider.setCuisine(c),
              ),
            ),
            const Spacer(),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                ElevatedButton(
                  onPressed: () => Navigator.pop(context),
                  child: const Text('뒤로가기'),
                ),
                ElevatedButton(
                  onPressed: provider.currentRequest.cuisine != null
                      ? () => Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (_) => const BudgetScreen(),
                          ),
                        )
                      : null,
                  child: const Text('다음'),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}

// --- 1-2번 화면: 예산입력 ---
class BudgetScreen extends StatelessWidget {
  const BudgetScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final provider = context.read<RecipeProvider>();
    return Scaffold(
      appBar: AppBar(title: const Text('1-2예산입력')),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          children: [
            TextField(
              decoration: InputDecoration(
                hintText: '예산입력창 <txt>',
                filled: true,
                fillColor: Colors.grey[300],
              ),
              keyboardType: TextInputType.number,
              onChanged: (val) => provider.setBudget(int.tryParse(val) ?? 0),
            ),
            const Text(
              '*테스트: 1000원 미만 입력시 에러 화면 표시*',
              style: TextStyle(color: Colors.red, fontSize: 12),
            ),
            const Spacer(),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                ElevatedButton(
                  onPressed: () => Navigator.pop(context),
                  child: const Text('뒤로'),
                ),
                ElevatedButton(
                  onPressed: () => Navigator.push(
                    context,
                    MaterialPageRoute(builder: (_) => const DifficultyScreen()),
                  ),
                  child: const Text('다음'),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}

// --- 1-3번 화면: 요리난이도 ---
class DifficultyScreen extends StatelessWidget {
  const DifficultyScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final provider = context.watch<RecipeProvider>();
    final diffs = ['설거지 최소화', '전자레인지', '요리초보', '10분완성'];

    return Scaffold(
      appBar: AppBar(title: const Text('1-3 요리난이도')),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          children: [
            ...diffs.map(
              (d) => GreyButton(
                text: d,
                isSelected: provider.currentRequest.difficulty == d,
                onPressed: () => provider.setDifficulty(d),
              ),
            ),
            const Spacer(),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                ElevatedButton(
                  onPressed: () => Navigator.pop(context),
                  child: const Text('뒤로'),
                ),
                ElevatedButton(
                  onPressed: provider.currentRequest.difficulty != null
                      ? () => Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (_) => const IngredientScreen(),
                          ),
                        )
                      : null,
                  child: const Text('다음'),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}

// --- 1-4번 화면: 재료추가 및 API 통신 분기 ---
class IngredientScreen extends StatelessWidget {
  const IngredientScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final provider = context.watch<RecipeProvider>();

    return Scaffold(
      appBar: AppBar(title: const Text('1-4 넣고싶은재료추가')),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          children: [
            TextField(
              decoration: InputDecoration(
                hintText: '넣고싶은재료추가 <txt>',
                filled: true,
                fillColor: Colors.grey[300],
              ),
              onChanged: (val) =>
                  context.read<RecipeProvider>().setIngredients(val),
            ),
            const Spacer(),

            // 화면 Loading 상태 처리
            if (provider.isLoading) const CircularProgressIndicator(),

            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                ElevatedButton(
                  onPressed: () => Navigator.pop(context),
                  child: const Text('뒤로'),
                ),
                ElevatedButton(
                  onPressed: provider.isLoading
                      ? null
                      : () async {
                          // 백엔드 API 요청 로직
                          bool success = await context
                              .read<RecipeProvider>()
                              .submitSearch();

                          // [수정됨] StatelessWidget에서는 context.mounted를 확인해야 함
                          if (!context.mounted) return;

                          if (success) {
                            Navigator.push(
                              context,
                              MaterialPageRoute(
                                builder: (_) => const RecommendationScreen(),
                              ),
                            );
                          } else {
                            Navigator.push(
                              context,
                              MaterialPageRoute(
                                builder: (_) => const ErrorScreen(),
                              ),
                            );
                          }
                        },
                  child: const Text('다음 (API 요청)'),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}

// --- 1-4-1번 화면: 분기점 오류메세지 ---
class ErrorScreen extends StatelessWidget {
  const ErrorScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final errorMsg = context.read<RecipeProvider>().errorMessage ?? '알 수 없는 오류';
    return Scaffold(
      appBar: AppBar(title: const Text('1-4-1 오류메세지')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Container(
              padding: const EdgeInsets.all(50),
              color: Colors.grey[300],
              child: Text(errorMsg),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: () =>
                  Navigator.popUntil(context, (route) => route.isFirst),
              child: const Text('확인버튼(홈화면으로 돌아가짐)'),
            ),
          ],
        ),
      ),
    );
  }
}

// --- 1-5번 화면: 요리추천 ---
class RecommendationScreen extends StatelessWidget {
  const RecommendationScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final recipes = context.watch<RecipeProvider>().recommendedRecipes;

    return Scaffold(
      appBar: AppBar(title: const Text('1-5 요리추천')),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          children: [
            Expanded(
              child: GridView.builder(
                gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                  crossAxisCount: 2,
                  childAspectRatio: 0.8,
                  crossAxisSpacing: 10,
                  mainAxisSpacing: 10,
                ),
                itemCount: recipes.length,
                itemBuilder: (context, index) {
                  return GestureDetector(
                    onTap: () {
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (_) =>
                              RecipeDetailScreen(recipe: recipes[index]),
                        ),
                      );
                    },
                    child: Column(
                      children: [
                        Container(
                          height: 30,
                          color: Colors.grey[300],
                          child: Center(child: Text(recipes[index].title)),
                        ),
                        Expanded(
                          child: Container(
                            color: Colors.grey[400],
                            child: const Center(child: Text('요리사진')),
                          ),
                        ),
                      ],
                    ),
                  );
                },
              ),
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                ElevatedButton(
                  onPressed: () => Navigator.pop(context),
                  child: const Text('뒤로'),
                ),
                ElevatedButton(
                  onPressed: () => Navigator.push(
                    context,
                    MaterialPageRoute(builder: (_) => const LinkScreen()),
                  ),
                  child: const Text('다음'),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}

// --- 1-6 / 2-2번 화면: 요리레시피 상세 ---
class RecipeDetailScreen extends StatelessWidget {
  final Recipe recipe;
  const RecipeDetailScreen({Key? key, required this.recipe}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('1-6 / 2-2 요리레시피')),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              recipe.title,
              style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 20),
            Text(recipe.description),
            const Spacer(),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                ElevatedButton(
                  onPressed: () {},
                  child: const Text('레시피생성하기\n(저장하기)'),
                ),
                ElevatedButton(
                  onPressed: () => Navigator.push(
                    context,
                    MaterialPageRoute(builder: (_) => const LinkScreen()),
                  ),
                  child: const Text('다음(최저가링크)'),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}

// --- 1-7번 화면: 최저가 링크 ---
class LinkScreen extends StatelessWidget {
  const LinkScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('1-7 최저가링크')),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          children: [
            const Expanded(child: Text('최저가링크들뜨게함\n~~~~~~~~~~~~~~~~')),
            ElevatedButton(
              onPressed: () =>
                  Navigator.popUntil(context, (route) => route.isFirst),
              child: const Text('홈화면'),
            ),
          ],
        ),
      ),
    );
  }
}

// --- 2-1번 화면: 레시피함 ---
class RecipeBoxScreen extends StatefulWidget {
  const RecipeBoxScreen({Key? key}) : super(key: key);

  @override
  State<RecipeBoxScreen> createState() => _RecipeBoxScreenState();
}

class _RecipeBoxScreenState extends State<RecipeBoxScreen> {
  @override
  void initState() {
    super.initState();
    // 진입 시 가짜 API로 저장된 데이터 불러오기
    WidgetsBinding.instance.addPostFrameCallback((_) {
      context.read<RecipeProvider>().loadSavedRecipes("");
    });
  }

  @override
  Widget build(BuildContext context) {
    final provider = context.watch<RecipeProvider>();

    return Scaffold(
      appBar: AppBar(title: const Text('2-1 레시피함')),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          children: [
            TextField(
              decoration: InputDecoration(
                hintText: '요리 이름입력하는곳(검색기능)',
                filled: true,
                fillColor: Colors.grey[300],
              ),
              onSubmitted: (val) => provider.loadSavedRecipes(val),
            ),
            const SizedBox(height: 20),
            Expanded(
              child: provider.isLoading
                  ? const Center(child: CircularProgressIndicator())
                  : provider.savedRecipes.isEmpty
                  ? const Center(child: Text('저장된 레시피가 없습니다.'))
                  : GridView.builder(
                      gridDelegate:
                          const SliverGridDelegateWithFixedCrossAxisCount(
                            crossAxisCount: 2,
                            childAspectRatio: 0.8,
                            crossAxisSpacing: 10,
                            mainAxisSpacing: 10,
                          ),
                      itemCount: provider.savedRecipes.length,
                      itemBuilder: (context, index) {
                        final recipe = provider.savedRecipes[index];
                        return GestureDetector(
                          onTap: () {
                            Navigator.push(
                              context,
                              MaterialPageRoute(
                                builder: (_) =>
                                    RecipeDetailScreen(recipe: recipe),
                              ),
                            );
                          },
                          child: Column(
                            children: [
                              Container(
                                height: 30,
                                color: Colors.grey[300],
                                child: Center(child: Text(recipe.title)),
                              ),
                              Expanded(
                                child: Container(
                                  color: Colors.grey[400],
                                  child: const Center(child: Text('요리사진')),
                                ),
                              ),
                            ],
                          ),
                        );
                      },
                    ),
            ),
            ElevatedButton(
              onPressed: () =>
                  Navigator.popUntil(context, (route) => route.isFirst),
              child: const Text('홈화면'),
            ),
          ],
        ),
      ),
    );
  }
}
