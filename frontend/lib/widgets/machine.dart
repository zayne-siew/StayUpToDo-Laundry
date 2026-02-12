import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:stay_up_to_do_laundry/models/machine.dart';
import 'package:url_launcher/url_launcher.dart';

export 'package:stay_up_to_do_laundry/models/machine.dart';

/// Design a box-like clickable component that appears as a simple square
/// on-screen with a centered textbox and a notification-style optional icon
/// in its top-right corner.
///
/// This component's function is to keep track of the state of a given
/// washer/dryer machine. It needs to store its ID (block + type + number;
/// e.g., 57D10, 55W6), status (available, paid for, in use, pending unload,
/// out-of-order), status history (status changes and corresponding user).
/// When in-use, the textbox will be shown displaying the remaining time in
/// format MM:SS; when out-of-order, the textbox will show red text
/// "Out Of Order"; else, it will be hidden. The top-right icon should show
/// green for available, yellow for pending unload, blue for paid for, and
/// red otherwise. Clicking on the component displays a popup-box with all
/// the information above, plus an optional additional section that displays
/// a telegram message and links to it.
class MachineWidget extends StatefulWidget {
  final MachineModel machine;
  final VoidCallback? onTap;

  const MachineWidget({super.key, required this.machine, this.onTap});

  @override
  State<MachineWidget> createState() => _MachineWidgetState();
}

class _MachineWidgetState extends State<MachineWidget> {
  void _showMachineDetails() {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
          title: Row(
            children: [
              Expanded(
                child: Text(
                  'Block ${widget.machine.blockNumber} ${widget.machine.type == MachineType.washer ? 'Washer' : 'Dryer'} ${widget.machine.number}',
                ),
              ),
              IconButton(
                icon: const Icon(Icons.close),
                onPressed: () => Navigator.of(context).pop(),
                padding: EdgeInsets.zero,
                constraints: const BoxConstraints(),
              ),
            ],
          ),
          content: SingleChildScrollView(
            child: Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                _buildInfoRow('Status', widget.machine.formattedStatus),
                if (widget.machine.remainingTimeSeconds != null)
                  _buildInfoRow(
                    'Remaining Time',
                    widget.machine.formattedRemainingTime,
                  ),
                const Divider(height: 24),
                const Text(
                  'Status History',
                  style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
                ),
                const SizedBox(height: 4),
                if (widget.machine.statusHistory.isEmpty)
                  Padding(
                    padding: const EdgeInsets.symmetric(vertical: 8),
                    child: const Text(
                      'No history to show',
                      style: TextStyle(
                        fontSize: 12,
                        fontWeight: FontWeight.w400,
                        color: Colors.black54,
                      ),
                    ),
                  ),
                ...widget.machine.statusHistory.map(
                  (entry) => Padding(
                    padding: const EdgeInsets.symmetric(vertical: 4),
                    child: Text(
                      '${entry.timestamp.toString().substring(0, 16)} - ${entry.formattedStatus} by ${entry.user}',
                      style: const TextStyle(fontSize: 12),
                    ),
                  ),
                ),
                if (widget.machine.telegramMessage != null) ...[
                  const Divider(height: 24),
                  const Text(
                    'Telegram Message',
                    style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
                  ),
                  const SizedBox(height: 8),
                  Text(widget.machine.telegramMessage!.message),
                  if (widget.machine.telegramMessage!.messageUrl != null)
                    TextButton(
                      onPressed: () {
                        final url = widget.machine.telegramMessage!.messageUrl!;
                        launchUrl(Uri.parse(url));
                      },
                      child: const Text('Open in Telegram'),
                    ),
                ],
              ],
            ),
          ),
        );
      },
    );
  }

  Widget _buildInfoRow(String label, String value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          SizedBox(
            width: 120,
            child: Text(
              '$label:',
              style: const TextStyle(fontWeight: FontWeight.bold),
            ),
          ),
          Expanded(child: Text(value)),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () {
        _showMachineDetails();
        widget.onTap?.call();
      },
      child: Container(
        width: 100,
        height: 100,
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(4),
          border: Border.all(
            color: widget.machine.type == MachineType.washer
                ? Colors.blue
                : Colors.red,
            width: 2,
          ),
          boxShadow: const [
            BoxShadow(
              color: Color.fromRGBO(0, 0, 0, 0.1),
              blurRadius: 4,
              offset: Offset(0, 2),
            ),
          ],
        ),
        child: Stack(
          children: [
            // Main content area
            Container(
              width: double.infinity,
              height: double.infinity,
              alignment: Alignment.center,
              child: Padding(
                padding: const EdgeInsets.all(12),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  crossAxisAlignment: CrossAxisAlignment.center,
                  children: [
                    // Machine ID (without block prefix)
                    Text(
                      '${widget.machine.type == MachineType.washer ? 'W' : 'D'}${widget.machine.number}',
                      style: GoogleFonts.interTight(
                        fontSize: 16,
                        fontWeight: FontWeight.bold,
                        color: Colors.black87,
                      ),
                    ),
                    const SizedBox(height: 4),
                    // Display text (time or error message)
                    if (widget.machine.shouldShowText)
                      Text(
                        widget.machine.displayText,
                        textAlign: TextAlign.center,
                        style: GoogleFonts.interTight(
                          fontSize:
                              widget.machine.status == MachineStatus.outOfOrder
                              ? 14
                              : 18,
                          fontWeight: FontWeight.w600,
                          color: widget.machine.displayTextColor,
                        ),
                      ),
                  ],
                ),
              ),
            ),
            // Status indicator (top-right corner)
            Positioned(
              top: 6,
              right: 6,
              child: Container(
                width: 16,
                height: 16,
                decoration: BoxDecoration(
                  color: widget.machine.statusColor,
                  shape: BoxShape.circle,
                  border: Border.all(color: Colors.white, width: 2),
                  boxShadow: const [
                    BoxShadow(
                      color: Color.fromRGBO(0, 0, 0, 0.2),
                      blurRadius: 2,
                      offset: Offset(0, 1),
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
