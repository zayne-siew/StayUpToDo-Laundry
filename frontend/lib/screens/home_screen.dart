import 'package:flutter/material.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:stay_up_to_do_laundry/widgets/machine.dart';
import 'package:stay_up_to_do_laundry/services/machine.dart';

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});

  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  // Machines from backend
  List<MachineModel> machines = [];

  // Loading state
  bool isLoading = true;
  String? errorMessage;

  // Sample user data
  final String userName = 'Zayne Siew';
  final String telegramUsername =
      '@${dotenv.env['TELEGRAM_USERNAME'] ?? 'zayne-siew'}';

  // Selected block number
  int selectedBlock = 55;

  // Machine service
  final MachineService machineService = MachineService(
    baseUrl: 'http://localhost:8000/api',
  );

  @override
  void initState() {
    super.initState();
    _loadMachines();
  }

  Future<void> _loadMachines() async {
    setState(() {
      isLoading = true;
      errorMessage = null;
    });

    try {
      final fetchedMachines = await machineService.getAllMachines();
      setState(() {
        machines = fetchedMachines;
        isLoading = false;
      });
    } catch (e) {
      setState(() {
        errorMessage = 'Failed to load machines: $e';
        isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.black87,
        elevation: 2,
        shadowColor: Colors.black.withOpacity(0.1),
        leading: Container(
          padding: const EdgeInsets.only(top: 8.0, bottom: 8.0, left: 16.0),
          child: Image.asset(
            'assets/images/sutd-logo.png',
            fit: BoxFit.contain,
          ),
        ),
        title: Row(
          children: [
            RichText(
              text: TextSpan(
                children: [
                  // Stay
                  TextSpan(
                    text: 'S',
                    style: GoogleFonts.interTight(
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                      fontStyle: FontStyle.italic,
                      color: Colors.white,
                    ),
                  ),
                  TextSpan(
                    text: 'tay',
                    style: GoogleFonts.interTight(
                      fontSize: 8,
                      fontWeight: FontWeight.normal,
                      fontStyle: FontStyle.italic,
                      color: Colors.white,
                    ),
                  ),

                  // Up
                  TextSpan(
                    text: 'U',
                    style: GoogleFonts.interTight(
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                      fontStyle: FontStyle.italic,
                      color: Colors.white,
                    ),
                  ),
                  TextSpan(
                    text: 'p',
                    style: GoogleFonts.interTight(
                      fontSize: 8,
                      fontWeight: FontWeight.normal,
                      fontStyle: FontStyle.italic,
                      color: Colors.white,
                    ),
                  ),

                  // To
                  TextSpan(
                    text: 'T',
                    style: GoogleFonts.interTight(
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                      fontStyle: FontStyle.italic,
                      color: Colors.white,
                    ),
                  ),
                  TextSpan(
                    text: 'o',
                    style: GoogleFonts.interTight(
                      fontSize: 8,
                      fontWeight: FontWeight.normal,
                      fontStyle: FontStyle.italic,
                      color: Colors.white,
                    ),
                  ),

                  // Do
                  TextSpan(
                    text: 'D',
                    style: GoogleFonts.interTight(
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                      fontStyle: FontStyle.italic,
                      color: Colors.white,
                    ),
                  ),
                  TextSpan(
                    text: 'o',
                    style: GoogleFonts.interTight(
                      fontSize: 8,
                      fontWeight: FontWeight.normal,
                      fontStyle: FontStyle.italic,
                      color: Colors.white,
                    ),
                  ),

                  // Laundry
                  TextSpan(
                    text: ' Laundry',
                    style: GoogleFonts.interTight(
                      fontSize: 16,
                      fontWeight: FontWeight.normal,
                      fontStyle: FontStyle.italic,
                      color: Colors.white,
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
        actions: [
          PopupMenuButton<String>(
            offset: const Offset(0, 50),
            tooltip: '',
            icon: Container(
              padding: const EdgeInsets.all(8),
              decoration: BoxDecoration(
                color: Colors.white,
                shape: BoxShape.circle,
              ),
              child: const Icon(Icons.person, color: Colors.black87, size: 16),
            ),
            itemBuilder: (BuildContext context) => [
              PopupMenuItem<String>(
                enabled: false,
                height: 60,
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      userName,
                      style: GoogleFonts.interTight(
                        fontSize: 14,
                        fontWeight: FontWeight.bold,
                        color: Colors.black87,
                      ),
                    ),
                    const SizedBox(height: 2),
                    Text(
                      telegramUsername,
                      style: GoogleFonts.interTight(
                        fontSize: 11,
                        color: Colors.grey,
                      ),
                    ),
                    const SizedBox(height: 6),
                    const Divider(height: 8, thickness: 1),
                  ],
                ),
              ),
              PopupMenuItem<String>(
                value: 'logout',
                height: 44,
                child: Row(
                  children: [
                    const Icon(Icons.logout, size: 16, color: Colors.red),
                    const SizedBox(width: 8),
                    Text(
                      'Logout',
                      style: GoogleFonts.interTight(
                        fontSize: 13,
                        color: Colors.red,
                      ),
                    ),
                  ],
                ),
              ),
            ],
            onSelected: (String value) {
              if (value == 'logout') {
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(
                    content: Text('This is a demo, unable to logout.'),
                    duration: Duration(seconds: 2),
                  ),
                );
              }
            },
          ),
        ],
      ),
      body: isLoading
          ? const Center(child: CircularProgressIndicator())
          : errorMessage != null
          ? Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Icon(Icons.error_outline, size: 48, color: Colors.red),
                  const SizedBox(height: 16),
                  Text(
                    errorMessage!,
                    style: GoogleFonts.interTight(
                      fontSize: 16,
                      color: Colors.red,
                    ),
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(height: 16),
                  ElevatedButton(
                    onPressed: _loadMachines,
                    child: const Text('Retry'),
                  ),
                ],
              ),
            )
          : _buildRoomLayout(selectedBlock),
    );
  }

  Widget _buildRoomLayout(int blockNumber) {
    final blockMachines = machines
        .where((m) => m.blockNumber == blockNumber)
        .toList();

    // Helper function to get machine by ID
    MachineModel? getMachine(String suffix) {
      try {
        return blockMachines.firstWhere((m) => m.id == '$blockNumber$suffix');
      } catch (e) {
        return null;
      }
    }

    const machineSize = 100.0;
    const spacing = 12.0;
    const roomWidth =
        machineSize * 5 + spacing * 7 + 110; // Fixed width for the room layout
    const roomHeight = machineSize * 4 + spacing * 5 + 60;

    return Center(
      child: ScrollConfiguration(
        behavior: ScrollConfiguration.of(context).copyWith(scrollbars: false),
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              // Title with dropdown
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  DropdownButton<int>(
                    value: selectedBlock,
                    underline: Container(),
                    icon: const Icon(Icons.arrow_drop_down, size: 28),
                    style: GoogleFonts.interTight(
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                      color: Colors.black,
                    ),
                    items: [55, 57, 59].map((int block) {
                      return DropdownMenuItem<int>(
                        value: block,
                        child: Text('Block $block Laundry Room'),
                      );
                    }).toList(),
                    onChanged: (int? newValue) {
                      if (newValue != null) {
                        setState(() {
                          selectedBlock = newValue;
                        });
                      }
                    },
                  ),
                ],
              ),
              const SizedBox(height: 12),
              // Legend row
              Wrap(
                spacing: 16,
                runSpacing: 8,
                alignment: WrapAlignment.center,
                children: [
                  _buildLegendItem(Colors.green, 'Available'),
                  _buildLegendItem(Colors.blue, 'Paid For'),
                  _buildLegendItem(Colors.yellow, 'Pending Unload'),
                  _buildLegendItem(Colors.red, 'In Use / Out of Order'),
                ],
              ),
              const SizedBox(height: 24),

              // Room layout container - horizontally scrollable
              ScrollConfiguration(
                behavior: ScrollConfiguration.of(
                  context,
                ).copyWith(scrollbars: false),
                child: SingleChildScrollView(
                  scrollDirection: Axis.horizontal,
                  child: Container(
                    width: roomWidth,
                    height: roomHeight,
                    padding: const EdgeInsets.all(20),
                    decoration: BoxDecoration(
                      color: Colors.white,
                      borderRadius: BorderRadius.circular(12),
                      border: Border.all(color: Colors.black, width: 2),
                    ),
                    child: Stack(
                      children: [
                        // Left wall - W1-W4
                        ..._buildMachineColumn(
                          [
                            getMachine('W1'),
                            getMachine('W2'),
                            getMachine('W3'),
                            getMachine('W4'),
                          ],
                          20,
                          20,
                          machineSize,
                          spacing,
                        ),

                        // Second column - W5-W8
                        ..._buildMachineColumn(
                          [
                            getMachine('W5'),
                            getMachine('W6'),
                            getMachine('W7'),
                            getMachine('W8'),
                          ],
                          20 + machineSize + spacing,
                          20,
                          machineSize,
                          spacing,
                        ),

                        // Third column - W9-W11
                        ..._buildMachineColumn(
                          [
                            getMachine('W9'),
                            getMachine('W10'),
                            getMachine('W11'),
                            getMachine('D1'),
                          ],
                          20 + (machineSize + spacing) * 2 + 60,
                          20,
                          machineSize,
                          spacing,
                        ),

                        // Fourth column - D2
                        ..._buildMachineColumn(
                          [getMachine('D2')],
                          20 + (machineSize + spacing) * 3 + 60,
                          20 + (machineSize + spacing) * 3,
                          machineSize,
                          spacing,
                        ),

                        // Last column - D3-D6`
                        ..._buildMachineColumn(
                          [
                            getMachine('D6'),
                            getMachine('D5'),
                            getMachine('D4'),
                            getMachine('D3'),
                          ],
                          20 + (machineSize + spacing) * 4 + 60,
                          20,
                          machineSize,
                          spacing,
                        ),
                      ],
                    ),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  List<Widget> _buildMachineColumn(
    List<MachineModel?> machines,
    double left,
    double top,
    double size,
    double spacing,
  ) {
    List<Widget> widgets = [];
    for (int i = 0; i < machines.length; i++) {
      final machine = machines[i];
      if (machine != null) {
        widgets.add(
          Positioned(
            left: left,
            top: top + i * (size + spacing),
            child: MachineWidget(
              machine: machine,
              onTap: () {
                print('Tapped machine: ${machine.id}'); // TODO: debug
              },
            ),
          ),
        );
      }
    }
    return widgets;
  }

  Widget _buildLegendItem(Color color, String label) {
    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        Container(
          width: 16,
          height: 16,
          decoration: BoxDecoration(
            color: color,
            shape: BoxShape.circle,
            border: Border.all(color: Colors.white, width: 2),
          ),
        ),
        const SizedBox(width: 8),
        Text(label, style: GoogleFonts.interTight(fontSize: 13)),
      ],
    );
  }
}
