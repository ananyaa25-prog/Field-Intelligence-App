import 'package:flutter/material.dart';
import 'package:camera/camera.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

// ================================================================
// PLANT INFORMATION MODEL
// ================================================================

class PlantInfo {
  final String name;
  final String description;
  final String questionType;
  final bool grounded;

  PlantInfo({
    required this.name,
    required this.description,
    required this.questionType,
    required this.grounded,
  });
}

// ================================================================
// VERIFIED PLANT DATA FOR SPECIES COMPARISON
//
// This is intentionally kept in main.dart so the comparison feature
// does not require another JSON modification.
// ================================================================

final Map<String, Map<String, String>> plantComparisonData = {
  'Tulasi': {
    'scientific': 'Ocimum tenuiflorum',
    'family': 'Lamiaceae',
    'habitat': 'Warm tropical and subtropical environments',
    'conservation': 'Not currently considered globally threatened',
  },
  'Neem': {
    'scientific': 'Azadirachta indica',
    'family': 'Meliaceae',
    'habitat': 'Tropical and subtropical regions',
    'conservation': 'Not currently considered globally threatened',
  },
  'Banyan': {
    'scientific': 'Ficus benghalensis',
    'family': 'Moraceae',
    'habitat': 'Tropical and subtropical environments',
    'conservation': 'Not currently considered globally threatened',
  },
  'Hibiscus': {
    'scientific': 'Hibiscus rosa-sinensis',
    'family': 'Malvaceae',
    'habitat': 'Warm tropical and subtropical environments',
    'conservation': 'Not currently considered globally threatened',
  },
  'Rose': {
    'scientific': 'Rosa spp.',
    'family': 'Rosaceae',
    'habitat': 'Gardens and temperate to subtropical environments',
    'conservation': 'Varies by species',
  },
  'Aloe Vera': {
    'scientific': 'Aloe vera',
    'family': 'Asphodelaceae',
    'habitat': 'Dry and semi-arid environments',
    'conservation': 'Not currently considered globally threatened',
  },
  'Sunflower': {
    'scientific': 'Helianthus annuus',
    'family': 'Asteraceae',
    'habitat': 'Open sunny areas and cultivated environments',
    'conservation': 'Not currently considered globally threatened',
  },
};

// ================================================================
// PLANTNET PLANT IDENTIFICATION
// ================================================================

Future<PlantInfo> identifyPlantFromCamera(
  String imagePath,
) async {
  const apiKey = '2b10aHjjU2TJJg3F3I2R0i3aO';

  final uri = Uri.parse(
    'https://my-api.plantnet.org/v2/identify/all'
    '?api-key=$apiKey'
    '&lang=en'
    '&nb-results=5',
  );

  final request = http.MultipartRequest(
    'POST',
    uri,
  );

  request.files.add(
    await http.MultipartFile.fromPath(
      'images',
      imagePath,
    ),
  );

  request.fields['organs'] = 'auto';

  final streamedResponse = await request.send();

  final response = await http.Response.fromStream(
    streamedResponse,
  );

  if (response.statusCode != 200) {
    throw Exception(
      'PlantNet identification failed: '
      '${response.statusCode}\n'
      '${response.body}',
    );
  }

  final data = jsonDecode(response.body);

  if (data['results'] == null ||
      (data['results'] as List).isEmpty) {
    throw Exception(
      'No plant could be identified.',
    );
  }

  final bestMatch = data['results'][0];

  final score =
      (bestMatch['score'] as num).toDouble();

  final species =
      bestMatch['species']
          ['scientificNameWithoutAuthor'];

  final commonNames =
      bestMatch['species']['commonNames']
          as List<dynamic>?;

  final commonName =
      commonNames != null &&
              commonNames.isNotEmpty
          ? commonNames[0].toString()
          : species;

  final normalizedName =
      normalizePlantName(commonName);

  return PlantInfo(
    name: normalizedName,
    description:
        'Scientific name: $species\n\n'
        'Identification confidence: '
        '${(score * 100).toStringAsFixed(1)}%',
    questionType: 'plant identification',
    grounded: score >= 0.70,
  );
}

// ================================================================
// PLANT NAME NORMALIZATION
// ================================================================

String normalizePlantName(String plantName) {
  final name = plantName.toLowerCase().trim();

  // TULASI / HOLY BASIL
  if (name.contains('tulsi') ||
      name.contains('tulasi') ||
      name.contains('holy basil') ||
      name.contains('sacred basil')) {
    return 'Tulasi';
  }

  // HIBISCUS
  if (name.contains('hibiscus') ||
      name.contains('shoe flower') ||
      name.contains('china rose')) {
    return 'Hibiscus';
  }

  // ROSE
  if (name.contains('rose')) {
    return 'Rose';
  }

  // NEEM
  if (name.contains('neem') ||
      name.contains('azadirachta')) {
    return 'Neem';
  }

  // ALOE
  if (name.contains('aloe')) {
    return 'Aloe Vera';
  }

  // BANYAN
  if (name.contains('banyan') ||
      name.contains('ficus benghalensis')) {
    return 'Banyan';
  }

  // SUNFLOWER
  if (name.contains('sunflower') ||
      name.contains('helianthus annuus')) {
    return 'Sunflower';
  }

  return plantName;
}

// ================================================================
// NATIVE SPECIES CHECK
// ================================================================

bool isNativeFocusSpecies(String plantName) {
  final normalized =
      normalizePlantName(plantName).toLowerCase();

  const nativeSpecies = {
    'neem',
    'tulasi',
    'banyan',
  };

  return nativeSpecies.contains(normalized);
}

// ================================================================
// BOTANICAL AI
// ================================================================

Future<PlantInfo> askBotanicalAI(
  String plant,
  String question,
) async {
  final normalizedPlant =
      normalizePlantName(plant);

  final response = await http.post(
    Uri.parse(
      'http://172.20.10.2:5000/ask',
    ),
    headers: {
      'Content-Type': 'application/json',
    },
    body: jsonEncode({
      'plant': normalizedPlant,
      'question': question,
    }),
  );

  if (response.statusCode != 200) {
    throw Exception(
      'Botanical AI request failed: '
      '${response.statusCode}',
    );
  }

  final data = jsonDecode(response.body);

  if (data['status'] != 'success') {
    throw Exception(
      data['answer'] ??
          data['error'] ??
          'Botanical API returned an error.',
    );
  }

  return PlantInfo(
    name: data['plant'] ?? normalizedPlant,
    description:
        data['answer'] ??
            'No answer available.',
    questionType:
        data['question_type'] ??
            'general',
    grounded:
        data['grounded'] ?? false,
  );
}

// ================================================================
// MAIN
// ================================================================

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  cameras = await availableCameras();

  runApp(const MyApp());
}

late List<CameraDescription> cameras;

// ================================================================
// APP
// ================================================================

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Botanical AI',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: Colors.green,
        ),
        useMaterial3: true,
      ),
      home: const CameraScreen(),
    );
  }
}

// ================================================================
// CAMERA SCREEN
// ================================================================

class CameraScreen extends StatefulWidget {
  const CameraScreen({super.key});

  @override
  State<CameraScreen> createState() =>
      _CameraScreenState();
}

class _CameraScreenState
    extends State<CameraScreen> {

  late CameraController controller;

  // --------------------------------------------------------------
  // IDENTIFICATION
  // --------------------------------------------------------------

  PlantInfo? identifiedPlant;

  String? identifiedPlantName;

  // --------------------------------------------------------------
  // BOTANICAL AI
  // --------------------------------------------------------------

  PlantInfo? aiAnswer;

  // --------------------------------------------------------------
  // UI STATE
  // --------------------------------------------------------------

  bool isLoading = false;

  bool showQuestionBox = false;

  final TextEditingController questionController =
      TextEditingController();

  // ==============================================================
  // GAMIFICATION
  // ==============================================================

  int discoveryCount = 0;

  final Set<String> discoveredPlants = {};

  // ==============================================================
  // CAMERA INITIALIZATION
  // ==============================================================

  @override
  void initState() {
    super.initState();

    controller = CameraController(
      cameras[0],
      ResolutionPreset.medium,
    );

    controller.initialize().then((_) {
      if (!mounted) return;

      setState(() {});
    });
  }

  // ==============================================================
  // DISPOSE
  // ==============================================================

  @override
  void dispose() {
    controller.dispose();
    questionController.dispose();

    super.dispose();
  }

  // ==============================================================
  // BUILD
  // ==============================================================

  @override
  Widget build(BuildContext context) {

    if (!controller.value.isInitialized) {
      return const Scaffold(
        body: Center(
          child: CircularProgressIndicator(),
        ),
      );
    }

    return Scaffold(
      body: Stack(
        children: [

          // CAMERA PREVIEW
          SizedBox.expand(
            child: FittedBox(
              fit: BoxFit.cover,
              child: SizedBox(
                width:
                    controller.value.previewSize!.height,
                height:
                    controller.value.previewSize!.width,
                child: CameraPreview(controller),
              ),
            ),
          ),

          // GAMIFICATION BADGE
          Positioned(
            top: 50,
            right: 20,
            child: _buildDiscoveryBadge(),
          ),

          // LOADING
          if (isLoading)
            Container(
              color: Colors.black54,
              child: const Center(
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [

                    CircularProgressIndicator(
                      color: Colors.white,
                    ),

                    SizedBox(height: 15),

                    Text(
                      'Identifying plant...',
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: 18,
                      ),
                    ),
                  ],
                ),
              ),
            ),

          // IDENTIFICATION CARD
          if (identifiedPlant != null &&
              !isLoading &&
              aiAnswer == null &&
              !showQuestionBox)
            Positioned(
              left: 20,
              right: 20,
              bottom: 100,
              child:
                  _buildPlantIdentificationCard(),
            ),

          // AI ANSWER
          if (aiAnswer != null &&
              !isLoading)
            Positioned(
              left: 20,
              right: 20,
              bottom: 100,
              child:
                  _buildAIAnswerCard(),
            ),

          // QUESTION BOX
          if (showQuestionBox &&
              !isLoading)
            Positioned(
              left: 20,
              right: 20,
              bottom: 100,
              child:
                  _buildQuestionBox(),
            ),

          // CAMERA BUTTON
          if (identifiedPlant == null &&
              !isLoading)
            Positioned(
              bottom: 30,
              left: 0,
              right: 0,
              child: Center(
                child: FloatingActionButton(
                  heroTag: 'cameraButton',
                  onPressed: _takePhoto,
                  child: const Icon(
                    Icons.camera_alt,
                  ),
                ),
              ),
            ),

          // AI BUTTON
          if (identifiedPlant != null &&
              aiAnswer == null &&
              !showQuestionBox &&
              !isLoading)
            Positioned(
              right: 20,
              bottom: 30,
              child: FloatingActionButton(
                heroTag: 'aiButton',
                onPressed: () {
                  setState(() {
                    showQuestionBox = true;
                  });
                },
                backgroundColor: Colors.white,
                child: const Icon(
                  Icons.auto_awesome,
                  color: Colors.green,
                ),
              ),
            ),
        ],
      ),
    );
  }

  // ================================================================
  // GAMIFICATION BADGE
  // ================================================================

  Widget _buildDiscoveryBadge() {
    return Container(
      padding: const EdgeInsets.symmetric(
        horizontal: 14,
        vertical: 10,
      ),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius:
            BorderRadius.circular(20),
        boxShadow: const [
          BoxShadow(
            color: Colors.black26,
            blurRadius: 8,
          ),
        ],
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [

          const Icon(
            Icons.emoji_events,
            color: Colors.amber,
          ),

          const SizedBox(width: 6),

          Text(
            '$discoveryCount discovered',
            style: const TextStyle(
              fontWeight: FontWeight.bold,
            ),
          ),
        ],
      ),
    );
  }

  // ================================================================
  // NATIVE SPECIES HIGHLIGHT
  // ================================================================

  Widget _buildBiodiversityHighlight() {

    final plantName =
        identifiedPlantName ?? '';

    if (isNativeFocusSpecies(plantName)) {

      return Container(
        width: double.infinity,
        margin:
            const EdgeInsets.only(bottom: 12),
        padding:
            const EdgeInsets.all(12),
        decoration: BoxDecoration(
          color: Colors.green.shade50,
          borderRadius:
              BorderRadius.circular(15),
          border: Border.all(
            color: Colors.green.shade300,
          ),
        ),
        child: Row(
          children: [

            const Icon(
              Icons.eco,
              color: Colors.green,
              size: 28,
            ),

            const SizedBox(width: 10),

            const Expanded(
              child: Column(
                crossAxisAlignment:
                    CrossAxisAlignment.start,
                children: [

                  Text(
                    '🌿 Native Species Highlight',
                    style: TextStyle(
                      fontSize: 15,
                      fontWeight:
                          FontWeight.bold,
                      color: Colors.green,
                    ),
                  ),

                  SizedBox(height: 3),

                  Text(
                    'A native/local-focus species '
                    'for the project biodiversity '
                    'experience.',
                    style: TextStyle(
                      fontSize: 13,
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      );
    }

    return Container(
      width: double.infinity,
      margin:
          const EdgeInsets.only(bottom: 12),
      padding:
          const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: Colors.blueGrey.shade50,
        borderRadius:
            BorderRadius.circular(15),
      ),
      child: const Row(
        children: [

          Icon(
            Icons.public,
            color: Colors.blueGrey,
          ),

          SizedBox(width: 10),

          Expanded(
            child: Text(
              'Biodiversity information available '
              'through the botanical knowledge base.',
              style: TextStyle(
                fontSize: 13,
                fontWeight:
                    FontWeight.w600,
              ),
            ),
          ),
        ],
      ),
    );
  }

  // ================================================================
  // PLANT IDENTIFICATION CARD
  // ================================================================

  Widget _buildPlantIdentificationCard() {

    return Container(
      padding:
          const EdgeInsets.all(20),

      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius:
            BorderRadius.circular(25),

        boxShadow: const [
          BoxShadow(
            color: Colors.black26,
            blurRadius: 15,
            offset: Offset(0, 5),
          ),
        ],
      ),

      child: SingleChildScrollView(
        child: Column(
          crossAxisAlignment:
              CrossAxisAlignment.start,

          mainAxisSize:
              MainAxisSize.min,

          children: [

            Text(
              identifiedPlant!.name,
              style: const TextStyle(
                fontSize: 28,
                fontWeight:
                    FontWeight.bold,
                color: Colors.green,
              ),
            ),

            const SizedBox(height: 10),

            Text(
              identifiedPlant!.description,
              style: const TextStyle(
                fontSize: 16,
                color: Colors.black87,
              ),
            ),

            const SizedBox(height: 15),

            // NATIVE SPECIES
            _buildBiodiversityHighlight(),

            // CONFIDENCE
            Text(
              identifiedPlant!.grounded
                  ? '✓ Identification confident'
                  : '⚠ Low identification confidence',
              style: TextStyle(
                fontSize: 14,
                fontWeight:
                    FontWeight.bold,
                color:
                    identifiedPlant!.grounded
                        ? Colors.green
                        : Colors.orange,
              ),
            ),

            const SizedBox(height: 15),

            // ASK AI
            SizedBox(
              width: double.infinity,
              child:
                  ElevatedButton.icon(
                onPressed: () {
                  setState(() {
                    showQuestionBox = true;
                  });
                },
                icon: const Icon(
                  Icons.auto_awesome,
                ),
                label: const Text(
                  'Ask Botanical AI',
                ),
              ),
            ),

            const SizedBox(height: 8),

            // ====================================================
            // NEW SPECIES COMPARISON BUTTON
            // ====================================================

            SizedBox(
              width: double.infinity,
              child:
                  ElevatedButton.icon(
                onPressed:
                    _showSpeciesComparison,
                icon: const Icon(
                  Icons.compare_arrows,
                ),
                label: const Text(
                  'Compare Species',
                ),
              ),
            ),

            const SizedBox(height: 8),

            // SCAN ANOTHER
            SizedBox(
              width: double.infinity,
              child:
                  OutlinedButton(
                onPressed: _resetScan,
                child: const Text(
                  'Scan Another Plant',
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  // ================================================================
  // SPECIES COMPARISON
  // ================================================================

  void _showSpeciesComparison() {

    final currentPlant =
        normalizePlantName(
      identifiedPlantName ?? '',
    );

    final availablePlants =
        plantComparisonData.keys
            .where(
              (plant) => plant != currentPlant,
            )
            .toList();

    String selectedPlant =
        availablePlants.isNotEmpty
            ? availablePlants.first
            : '';

    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (context) {

        return StatefulBuilder(
          builder: (
            context,
            setModalState,
          ) {

            return Container(
              height:
                  MediaQuery.of(context)
                          .size
                          .height *
                      0.75,

              padding:
                  const EdgeInsets.all(20),

              decoration: const BoxDecoration(
                color: Colors.white,
                borderRadius:
                    BorderRadius.vertical(
                  top: Radius.circular(30),
                ),
              ),

              child: Column(
                crossAxisAlignment:
                    CrossAxisAlignment.start,

                children: [

                  // HEADER
                  Row(
                    children: [

                      const Icon(
                        Icons.compare_arrows,
                        color: Colors.green,
                        size: 30,
                      ),

                      const SizedBox(width: 10),

                      const Expanded(
                        child: Text(
                          'Compare Species',
                          style: TextStyle(
                            fontSize: 24,
                            fontWeight:
                                FontWeight.bold,
                            color: Colors.green,
                          ),
                        ),
                      ),

                      IconButton(
                        onPressed: () {
                          Navigator.pop(context);
                        },
                        icon: const Icon(
                          Icons.close,
                        ),
                      ),
                    ],
                  ),

                  const SizedBox(height: 8),

                  Text(
                    'Compare $currentPlant with another verified species.',
                    style: const TextStyle(
                      color: Colors.black54,
                    ),
                  ),

                  const SizedBox(height: 15),

                  // SPECIES SELECTOR
                  DropdownButtonFormField<String>(
                    value: selectedPlant,
                    decoration:
                        InputDecoration(
                      labelText:
                          'Select species',
                      border:
                          OutlineInputBorder(
                        borderRadius:
                            BorderRadius.circular(
                          15,
                        ),
                      ),
                    ),
                    items:
                        availablePlants
                            .map(
                      (plant) {
                        return DropdownMenuItem<
                            String>(
                          value: plant,
                          child:
                              Text(plant),
                        );
                      },
                    ).toList(),
                    onChanged: (value) {
                      if (value == null) {
                        return;
                      }

                      setModalState(() {
                        selectedPlant =
                            value;
                      });
                    },
                  ),

                  const SizedBox(height: 20),

                  // COMPARISON TABLE
                  Expanded(
                    child:
                        _buildComparisonTable(
                      currentPlant,
                      selectedPlant,
                    ),
                  ),
                ],
              ),
            );
          },
        );
      },
    );
  }

  // ================================================================
  // COMPARISON TABLE
  // ================================================================

  Widget _buildComparisonTable(
    String firstPlant,
    String secondPlant,
  ) {

    final first =
        plantComparisonData[firstPlant];

    final second =
        plantComparisonData[secondPlant];

    if (first == null ||
        second == null) {
      return const Center(
        child: Text(
          'Comparison information unavailable.',
        ),
      );
    }

    return SingleChildScrollView(
      child: Column(
        children: [

          _comparisonRow(
            'Species',
            firstPlant,
            secondPlant,
            isHeader: true,
          ),

          _comparisonRow(
            'Scientific name',
            first['scientific']!,
            second['scientific']!,
          ),

          _comparisonRow(
            'Family',
            first['family']!,
            second['family']!,
          ),

          _comparisonRow(
            'Habitat',
            first['habitat']!,
            second['habitat']!,
          ),

          _comparisonRow(
            'Conservation status',
            first['conservation']!,
            second['conservation']!,
          ),
        ],
      ),
    );
  }

  // ================================================================
  // COMPARISON ROW
  // ================================================================

  Widget _comparisonRow(
    String label,
    String firstValue,
    String secondValue, {
    bool isHeader = false,
  }) {

    return Container(
      margin:
          const EdgeInsets.only(bottom: 8),

      decoration: BoxDecoration(
        borderRadius:
            BorderRadius.circular(12),
        border: Border.all(
          color: Colors.grey.shade300,
        ),
      ),

      child: IntrinsicHeight(
        child: Row(
          crossAxisAlignment:
              CrossAxisAlignment.stretch,

          children: [

            // LABEL
            Container(
              width: 105,
              padding:
                  const EdgeInsets.all(10),
              decoration: BoxDecoration(
                color: Colors.green.shade50,
                borderRadius:
                    const BorderRadius.only(
                  topLeft:
                      Radius.circular(12),
                  bottomLeft:
                      Radius.circular(12),
                ),
              ),
              child: Text(
                label,
                style: TextStyle(
                  fontSize: 13,
                  fontWeight:
                      FontWeight.bold,
                  color:
                      isHeader
                          ? Colors.green
                          : Colors.black87,
                ),
              ),
            ),

            // FIRST VALUE
            Expanded(
              child: Padding(
                padding:
                    const EdgeInsets.all(10),
                child: Text(
                  firstValue,
                  style: const TextStyle(
                    fontSize: 13,
                    fontWeight:
                        FontWeight.w600,
                  ),
                ),
              ),
            ),

            // SECOND VALUE
            Expanded(
              child: Container(
                padding:
                    const EdgeInsets.all(10),
                decoration: BoxDecoration(
                  color:
                      Colors.grey.shade50,
                  borderRadius:
                      const BorderRadius.only(
                    topRight:
                        Radius.circular(12),
                    bottomRight:
                        Radius.circular(12),
                  ),
                ),
                child: Text(
                  secondValue,
                  style: const TextStyle(
                    fontSize: 13,
                    fontWeight:
                        FontWeight.w600,
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  // ================================================================
  // QUESTION BOX
  // ================================================================

  Widget _buildQuestionBox() {

    return Container(
      padding:
          const EdgeInsets.all(15),

      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius:
            BorderRadius.circular(20),

        boxShadow: const [
          BoxShadow(
            color: Colors.black26,
            blurRadius: 12,
            offset: Offset(0, 4),
          ),
        ],
      ),

      child: Column(
        crossAxisAlignment:
            CrossAxisAlignment.start,

        children: [

          Row(
            children: [

              const Icon(
                Icons.auto_awesome,
                color: Colors.green,
              ),

              const SizedBox(width: 8),

              const Expanded(
                child: Text(
                  'Botanical Assistant',
                  style: TextStyle(
                    fontSize: 19,
                    fontWeight:
                        FontWeight.bold,
                    color: Colors.green,
                  ),
                ),
              ),

              IconButton(
                onPressed: () {
                  setState(() {
                    showQuestionBox = false;
                  });
                },
                icon:
                    const Icon(Icons.close),
              ),
            ],
          ),

          const SizedBox(height: 5),

          Text(
            'Asking about: '
            '${identifiedPlantName ?? ''}',
            style: const TextStyle(
              fontSize: 14,
              fontWeight:
                  FontWeight.w600,
              color: Colors.black54,
            ),
          ),

          const SizedBox(height: 12),

          TextField(
            controller:
                questionController,

            autofocus: true,

            maxLines: 3,

            textInputAction:
                TextInputAction.done,

            decoration:
                InputDecoration(
              hintText:
                  'Ask something about this plant...',

              filled: true,

              fillColor:
                  Colors.grey.shade100,

              border:
                  OutlineInputBorder(
                borderRadius:
                    BorderRadius.circular(15),
                borderSide:
                    BorderSide.none,
              ),
            ),
          ),

          const SizedBox(height: 12),

          SizedBox(
            width: double.infinity,

            child:
                ElevatedButton.icon(
              onPressed:
                  _askBotanicalAI,

              icon: const Icon(
                Icons.send,
              ),

              label: const Text(
                'Ask Botanical AI',
              ),
            ),
          ),
        ],
      ),
    );
  }

  // ================================================================
  // AI ANSWER CARD
  // ================================================================

  Widget _buildAIAnswerCard() {

    return Container(
      padding:
          const EdgeInsets.all(20),

      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius:
            BorderRadius.circular(25),

        boxShadow: const [
          BoxShadow(
            color: Colors.black26,
            blurRadius: 15,
            offset: Offset(0, 5),
          ),
        ],
      ),

      child: SingleChildScrollView(
        child: Column(
          crossAxisAlignment:
              CrossAxisAlignment.start,

          mainAxisSize:
              MainAxisSize.min,

          children: [

            Row(
              children: [

                const Icon(
                  Icons.auto_awesome,
                  color: Colors.green,
                ),

                const SizedBox(width: 8),

                const Text(
                  'Botanical AI',
                  style: TextStyle(
                    fontSize: 20,
                    fontWeight:
                        FontWeight.bold,
                    color: Colors.green,
                  ),
                ),
              ],
            ),

            const SizedBox(height: 15),

            Text(
              identifiedPlantName ??
                  aiAnswer!.name,
              style: const TextStyle(
                fontSize: 18,
                fontWeight:
                    FontWeight.bold,
              ),
            ),

            const SizedBox(height: 10),

            Text(
              aiAnswer!.description,
              style: const TextStyle(
                fontSize: 16,
                color: Colors.black87,
              ),
            ),

            const SizedBox(height: 10),

            Text(
              'Question type: '
              '${aiAnswer!.questionType}',
              style: const TextStyle(
                fontSize: 14,
                fontWeight:
                    FontWeight.w600,
              ),
            ),

            const SizedBox(height: 5),

            Text(
              aiAnswer!.grounded
                  ? '✓ Knowledge grounded'
                  : '⚠ Knowledge not grounded',
              style: TextStyle(
                fontSize: 14,
                fontWeight:
                    FontWeight.bold,
                color:
                    aiAnswer!.grounded
                        ? Colors.green
                        : Colors.orange,
              ),
            ),

            const SizedBox(height: 15),

            SizedBox(
              width: double.infinity,

              child:
                  ElevatedButton.icon(
                onPressed: () {
                  setState(() {
                    aiAnswer = null;
                    showQuestionBox = true;
                    questionController.clear();
                  });
                },

                icon: const Icon(
                  Icons.question_answer,
                ),

                label: const Text(
                  'Ask Another Question',
                ),
              ),
            ),

            SizedBox(
              width: double.infinity,

              child:
                  OutlinedButton(
                onPressed:
                    _resetScan,

                child: const Text(
                  'Scan Another Plant',
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  // ================================================================
  // ASK BOTANICAL AI
  // ================================================================

  Future<void> _askBotanicalAI() async {

    final question =
        questionController.text.trim();

    if (question.isEmpty) {

      ScaffoldMessenger.of(context)
          .showSnackBar(
        const SnackBar(
          content: Text(
            'Please enter a question first.',
          ),
        ),
      );

      return;
    }

    if (identifiedPlantName == null) {

      ScaffoldMessenger.of(context)
          .showSnackBar(
        const SnackBar(
          content: Text(
            'Please scan a plant first.',
          ),
        ),
      );

      return;
    }

    setState(() {
      isLoading = true;
    });

    try {

      final result =
          await askBotanicalAI(
        identifiedPlantName!,
        question,
      );

      if (!mounted) return;

      setState(() {
        aiAnswer = result;
        isLoading = false;
        showQuestionBox = false;
      });

    } catch (e) {

      if (!mounted) return;

      setState(() {
        isLoading = false;
      });

      ScaffoldMessenger.of(context)
          .showSnackBar(
        SnackBar(
          content: Text(
            'Something went wrong: $e',
          ),
        ),
      );
    }
  }

  // ================================================================
  // TAKE PHOTO + IDENTIFY
  // ================================================================

  Future<void> _takePhoto() async {

    try {

      setState(() {
        isLoading = true;
      });

      final image =
          await controller.takePicture();

      final result =
          await identifyPlantFromCamera(
        image.path,
      );

      if (!mounted) return;

      // ============================================================
      // GAMIFIED DISCOVERY
      // ============================================================

      final canonicalName =
          normalizePlantName(
        result.name,
      );

      final discoveryKey =
          canonicalName.toLowerCase();

      final isNewDiscovery =
          !discoveredPlants.contains(
        discoveryKey,
      );

      if (isNewDiscovery) {

        discoveredPlants.add(
          discoveryKey,
        );

        discoveryCount++;

        String? badgeMessage;

        if (discoveryCount == 3) {

          badgeMessage =
              '🏆 Explorer Badge unlocked!';

        } else if (discoveryCount == 5) {

          badgeMessage =
              '🌿 Biodiversity Explorer Badge unlocked!';

        } else if (discoveryCount == 7) {

          badgeMessage =
              '🌎 Field Botanist Badge unlocked!';
        }

        if (badgeMessage != null) {

          WidgetsBinding.instance
              .addPostFrameCallback((_) {

            if (!mounted) return;

            ScaffoldMessenger.of(context)
                .showSnackBar(
              SnackBar(
                content:
                    Text(badgeMessage!),
              ),
            );
          });
        }
      }

      setState(() {

        identifiedPlant = result;

        identifiedPlantName =
            result.name;

        aiAnswer = null;

        showQuestionBox = false;

        isLoading = false;
      });

    } catch (e) {

      if (!mounted) return;

      setState(() {
        isLoading = false;
      });

      ScaffoldMessenger.of(context)
          .showSnackBar(
        SnackBar(
          content: Text(
            'Plant identification failed:\n$e',
          ),
        ),
      );
    }
  }

  // ================================================================
  // RESET
  // ================================================================

  void _resetScan() {

    setState(() {

      identifiedPlant = null;

      identifiedPlantName = null;

      aiAnswer = null;

      showQuestionBox = false;

      questionController.clear();
    });
  }
}