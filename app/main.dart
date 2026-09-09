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
// PL@NTNET PLANT IDENTIFICATION
//
// THIS FUNCTION IS ONLY FOR CAMERA IDENTIFICATION.
// It sends the captured image to Pl@ntNet.
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

  // Create multipart POST request.
  final request = http.MultipartRequest(
    'POST',
    uri,
  );

  // Add the camera image.
  request.files.add(
    await http.MultipartFile.fromPath(
      'images',
      imagePath,
    ),
  );

  // Let Pl@ntNet automatically determine whether
  // the image contains a leaf, flower, fruit, etc.
  request.fields['organs'] = 'auto';

  // Send request.
  final streamedResponse = await request.send();

  // Convert streamed response into normal HTTP response.
  final response = await http.Response.fromStream(
    streamedResponse,
  );

  if (response.statusCode != 200) {
    throw Exception(
      'Pl@ntNet identification failed: '
      '${response.statusCode}\n'
      '${response.body}',
    );
  }

  final data = jsonDecode(response.body);

  // Make sure results exist.
  if (data['results'] == null ||
      (data['results'] as List).isEmpty) {
    throw Exception(
      'No plant could be identified.',
    );
  }

  // Pl@ntNet returns results ordered by confidence.
  final bestMatch = data['results'][0];

  final score =
      (bestMatch['score'] as num).toDouble();

  final species =
      bestMatch['species']
          ['scientificNameWithoutAuthor'];

  // Try to get a common name.
  final commonNames =
      bestMatch['species']['commonNames']
          as List<dynamic>?;

  final commonName =
      commonNames != null &&
              commonNames.isNotEmpty
          ? commonNames[0].toString()
          : species;

  return PlantInfo(
    name: commonName,
    description:
        'Scientific name: $species\n\n'
        'Identification confidence: '
        '${(score * 100).toStringAsFixed(1)}%',
    questionType: 'plant identification',

    // This is OUR threshold for displaying
    // "high confidence". It is not an official
    // Pl@ntNet verification threshold.
    grounded: score >= 0.70,
  );
}


// ================================================================
// BOTANICAL AI
//
// THIS IS YOUR EXISTING FLASK /ask API.
// DO NOT CONFUSE THIS WITH PL@NTNET.
//
// It receives:
//   plant   -> plant identified by Pl@ntNet
//   question -> user's question
//
// ================================================================

Future<PlantInfo> askBotanicalAI(
  String plant,
  String question,
) async {
  final response = await http.post(
    Uri.parse(
      'http://172.20.10.2:5000/ask',
    ),
    headers: {
      'Content-Type': 'application/json',
    },
    body: jsonEncode({
      'plant': plant,
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
      data['answer']??
      data['error'] ??
          'Botanical API returned an error.',
    );
  }

  return PlantInfo(
    name: data['plant'] ?? plant,
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
  // PLANT IDENTIFICATION RESULT
  // --------------------------------------------------------------

  PlantInfo? identifiedPlant;

  // --------------------------------------------------------------
  // BOTANICAL AI RESULT
  // --------------------------------------------------------------

  PlantInfo? aiAnswer;

  // The actual plant name detected by Pl@ntNet.
  String? identifiedPlantName;

  // --------------------------------------------------------------
  // UI STATE
  // --------------------------------------------------------------

  bool isLoading = false;
  bool showQuestionBox = false;

  final TextEditingController questionController =
      TextEditingController();


  // ==============================================================
  // INITIALIZE CAMERA
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

          // ========================================================
          // CAMERA PREVIEW
          // ========================================================

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


          // ========================================================
          // LOADING INDICATOR
          // ========================================================

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
                      'Working...',
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: 18,
                      ),
                    ),
                  ],
                ),
              ),
            ),


          // ========================================================
          // PLANT IDENTIFICATION CARD
          // ========================================================

          if (identifiedPlant != null &&
              !isLoading &&
              aiAnswer == null)
            Positioned(
              left: 20,
              right: 20,
              bottom: 100,
              child: _buildPlantIdentificationCard(),
            ),


          // ========================================================
          // BOTANICAL AI ANSWER CARD
          // ========================================================

          if (aiAnswer != null &&
              !isLoading)
            Positioned(
              left: 20,
              right: 20,
              bottom: 100,
              child: _buildAIAnswerCard(),
            ),


          // ========================================================
          // BOTANICAL AI QUESTION BOX
          // ========================================================

          if (showQuestionBox &&
              !isLoading)
            Positioned(
              left: 20,
              right: 20,
              bottom: 100,
              child: _buildQuestionBox(),
            ),


          // ========================================================
          // AI BUTTON
          //
          // This stays available AFTER plant identification.
          // ========================================================

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


          // ========================================================
          // CAMERA BUTTON
          // ========================================================

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
        ],
      ),
    );
  }


  // ================================================================
  // PLANT IDENTIFICATION CARD
  // ================================================================

  Widget _buildPlantIdentificationCard() {
    return Container(
      padding: const EdgeInsets.all(20),

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

      child: Column(
        crossAxisAlignment:
            CrossAxisAlignment.start,

        mainAxisSize:
            MainAxisSize.min,

        children: [

          // --------------------------------------------------------
          // NAME
          // --------------------------------------------------------

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

          // --------------------------------------------------------
          // DESCRIPTION
          // --------------------------------------------------------

          Text(
            identifiedPlant!.description,
            style: const TextStyle(
              fontSize: 16,
              color: Colors.black87,
            ),
          ),

          const SizedBox(height: 10),

          // --------------------------------------------------------
          // CONFIDENCE
          // --------------------------------------------------------

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

          // --------------------------------------------------------
          // ASK AI BUTTON
          // --------------------------------------------------------

          SizedBox(
            width: double.infinity,
            child: ElevatedButton.icon(
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

          // --------------------------------------------------------
          // SCAN ANOTHER
          // --------------------------------------------------------

          SizedBox(
            width: double.infinity,
            child: OutlinedButton(
              onPressed: _resetScan,
              child: const Text(
                'Scan Another Plant',
              ),
            ),
          ),
        ],
      ),
    );
  }


  // ================================================================
  // BOTANICAL AI QUESTION BOX
  // ================================================================

  Widget _buildQuestionBox() {
    return Container(
      padding: const EdgeInsets.all(15),

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

          // --------------------------------------------------------
          // HEADER
          // --------------------------------------------------------

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
                icon: const Icon(
                  Icons.close,
                ),
              ),
            ],
          ),

          const SizedBox(height: 5),

          // --------------------------------------------------------
          // IDENTIFIED PLANT
          // --------------------------------------------------------

          Text(
            'Asking about: $identifiedPlantName',
            style: const TextStyle(
              fontSize: 14,
              fontWeight:
                  FontWeight.w600,
              color: Colors.black54,
            ),
          ),

          const SizedBox(height: 12),

          // --------------------------------------------------------
          // QUESTION
          // --------------------------------------------------------

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
                    BorderRadius.circular(
                        15),

                borderSide:
                    BorderSide.none,
              ),
            ),
          ),

          const SizedBox(height: 12),

          // --------------------------------------------------------
          // ASK BUTTON
          // --------------------------------------------------------

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
  // BOTANICAL AI ANSWER CARD
  // ================================================================

  Widget _buildAIAnswerCard() {
    return Container(
      padding: const EdgeInsets.all(20),

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

      child: Column(
        crossAxisAlignment:
            CrossAxisAlignment.start,

        mainAxisSize:
            MainAxisSize.min,

        children: [

          // --------------------------------------------------------
          // HEADER
          // --------------------------------------------------------

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

          // --------------------------------------------------------
          // PLANT
          // --------------------------------------------------------

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

          // --------------------------------------------------------
          // ANSWER
          // --------------------------------------------------------

          Text(
            aiAnswer!.description,
            style: const TextStyle(
              fontSize: 16,
              color: Colors.black87,
            ),
          ),

          const SizedBox(height: 10),

          // --------------------------------------------------------
          // QUESTION TYPE
          // --------------------------------------------------------

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

          // --------------------------------------------------------
          // GROUNDED STATUS
          //
          // THIS IS STILL FROM YOUR BOTANICAL AI.
          // We did NOT replace it with Pl@ntNet confidence.
          // --------------------------------------------------------

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

          // --------------------------------------------------------
          // ASK ANOTHER QUESTION
          // --------------------------------------------------------

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

          // --------------------------------------------------------
          // NEW PLANT
          // --------------------------------------------------------

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
    );
  }


  // ================================================================
  // ASK BOTANICAL AI
  // ================================================================

  Future<void> _askBotanicalAI() async {
    final question =
        questionController.text.trim();

    // --------------------------------------------------------------
    // CHECK QUESTION
    // --------------------------------------------------------------

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

    // --------------------------------------------------------------
    // CHECK THAT A PLANT WAS IDENTIFIED
    // --------------------------------------------------------------

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

      // IMPORTANT:
      // This goes to YOUR Flask Botanical AI,
      // NOT Pl@ntNet.

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
  // TAKE PHOTO + IDENTIFY WITH PL@NTNET
  // ================================================================

  Future<void> _takePhoto() async {
    try {

      setState(() {
        isLoading = true;
      });

      // ------------------------------------------------------------
      // TAKE PHOTO
      // ------------------------------------------------------------

      final image =
          await controller.takePicture();

      // ------------------------------------------------------------
      // SEND PHOTO TO PL@NTNET
      // ------------------------------------------------------------

      final result =
          await identifyPlantFromCamera(
        image.path,
      );

      if (!mounted) return;

      // ------------------------------------------------------------
      // SAVE IDENTIFICATION
      // ------------------------------------------------------------

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
  // RESET EVERYTHING AND SCAN ANOTHER PLANT
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