import 'package:flutter/material.dart';

/// Enum representing the status of a machine
enum MachineStatus { available, paidFor, inUse, pendingUnload, outOfOrder }

/// Enum representing the type of machine
enum MachineType { washer, dryer }

/// Model representing a status change entry in history
class StatusHistoryEntry {
  final MachineStatus status;
  final DateTime timestamp;
  final String user;

  StatusHistoryEntry({
    required this.status,
    required this.timestamp,
    required this.user,
  });

  /// Get formatted status string
  String get formattedStatus {
    switch (status) {
      case MachineStatus.available:
        return 'Available';
      case MachineStatus.paidFor:
        return 'Paid For';
      case MachineStatus.inUse:
        return 'In Use';
      case MachineStatus.pendingUnload:
        return 'Pending Unload';
      case MachineStatus.outOfOrder:
        return 'Out of Order';
    }
  }

  factory StatusHistoryEntry.fromJson(Map<String, dynamic> json) {
    return StatusHistoryEntry(
      status: MachineStatus.values.firstWhere(
        (e) => e.toString().split('.').last == json['status'],
      ),
      timestamp: DateTime.parse(json['timestamp']),
      user: json['user'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'status': status.toString().split('.').last,
      'timestamp': timestamp.toIso8601String(),
      'user': user,
    };
  }
}

/// Model representing a Telegram message notification
class TelegramMessage {
  final String message;
  final String? messageUrl;

  TelegramMessage({required this.message, this.messageUrl});

  factory TelegramMessage.fromJson(Map<String, dynamic> json) {
    return TelegramMessage(
      message: json['message'],
      messageUrl: json['message_url'],
    );
  }

  Map<String, dynamic> toJson() {
    return {'message': message, 'message_url': messageUrl};
  }
}

/// Main model representing a laundry machine
class MachineModel {
  final String id; // Format: "55W1"-"59D12" (block + type + number)
  final int blockNumber; // Must be one of: 55, 57, 59
  MachineStatus status;
  List<StatusHistoryEntry> statusHistory;
  String? estimatedFinishTime; // ISO 8601 UTC timestamp for inUse machines
  TelegramMessage? telegramMessage;

  static const List<int> validBlocks = [55, 57, 59];

  MachineModel({
    required this.id,
    required this.blockNumber,
    required this.status,
    this.statusHistory = const [],
    this.estimatedFinishTime,
    this.telegramMessage,
  }) {
    if (!validBlocks.contains(blockNumber)) {
      throw ArgumentError(
        'Block number must be one of $validBlocks, got $blockNumber',
      );
    }
  }

  /// Get machine type from ID (e.g., '57W4' -> washer)
  MachineType get type {
    if (id.contains('W')) return MachineType.washer;
    if (id.contains('D')) return MachineType.dryer;
    throw ArgumentError('Invalid machine ID format: $id');
  }

  /// Get machine number from ID (e.g., '57W4' -> 4)
  int get number {
    final match = RegExp(r'[WD](\d+)').firstMatch(id);
    if (match != null) {
      return int.parse(match.group(1)!);
    }
    throw ArgumentError('Invalid machine ID format: $id');
  }

  /// Calculate remaining time in seconds from estimated finish time
  int? get remainingTimeSeconds {
    if (estimatedFinishTime == null) return null;
    try {
      final finishTime = DateTime.parse(estimatedFinishTime!);
      final now = DateTime.now().toUtc();
      final difference = finishTime.difference(now).inSeconds;
      return difference > 0 ? difference : 0;
    } catch (e) {
      return null;
    }
  }

  /// Get formatted remaining time as MM:SS
  String get formattedRemainingTime {
    final seconds = remainingTimeSeconds;
    if (seconds == null) return '';
    final minutes = seconds ~/ 60;
    final secs = seconds % 60;
    return '${minutes.toString().padLeft(2, '0')}:${secs.toString().padLeft(2, '0')}';
  }

  /// Get formatted status as a proper string
  String get formattedStatus {
    switch (status) {
      case MachineStatus.available:
        return 'Available';
      case MachineStatus.paidFor:
        return 'Paid For';
      case MachineStatus.inUse:
        return 'In Use';
      case MachineStatus.pendingUnload:
        return 'Pending Unload';
      case MachineStatus.outOfOrder:
        return 'Out of Order';
    }
  }

  /// Get the color for the status indicator icon
  Color get statusColor {
    switch (status) {
      case MachineStatus.available:
        return Colors.green;
      case MachineStatus.pendingUnload:
        return Colors.yellow;
      case MachineStatus.paidFor:
        return Colors.blue;
      case MachineStatus.inUse:
      case MachineStatus.outOfOrder:
        return Colors.red;
    }
  }

  /// Check if the textbox should be shown
  bool get shouldShowText {
    return status == MachineStatus.inUse || status == MachineStatus.outOfOrder;
  }

  /// Get the text to display in the textbox
  String get displayText {
    if (status == MachineStatus.inUse) {
      return formattedRemainingTime;
    } else if (status == MachineStatus.outOfOrder) {
      return 'Out Of Order';
    }
    return '';
  }

  /// Get the text color for the display text
  Color get displayTextColor {
    return status == MachineStatus.outOfOrder ? Colors.red : Colors.black;
  }

  /// Update machine status and add to history
  void updateStatus(MachineStatus newStatus, String user) {
    status = newStatus;
    statusHistory.add(
      StatusHistoryEntry(
        status: newStatus,
        timestamp: DateTime.now(),
        user: user,
      ),
    );
  }

  /// Update estimated finish time (for in-use machines)
  void updateEstimatedFinishTime(String? finishTime) {
    estimatedFinishTime = finishTime;
  }

  /// Create from JSON (for API response parsing)
  factory MachineModel.fromJson(Map<String, dynamic> json) {
    return MachineModel(
      id: json['id'],
      blockNumber: json['block_number'],
      status: MachineStatus.values.firstWhere(
        (e) => e.toString().split('.').last == json['status'],
      ),
      statusHistory:
          (json['status_history'] as List<dynamic>?)
              ?.map((e) => StatusHistoryEntry.fromJson(e))
              .toList() ??
          [],
      estimatedFinishTime: json['estimated_finish_time'],
      telegramMessage: json['telegram_message'] != null
          ? TelegramMessage.fromJson(json['telegram_message'])
          : null,
    );
  }

  /// Convert to JSON (for API requests)
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'block_number': blockNumber,
      'status': status.toString().split('.').last,
      'status_history': statusHistory.map((e) => e.toJson()).toList(),
      'estimated_finish_time': estimatedFinishTime,
      'telegram_message': telegramMessage?.toJson(),
    };
  }

  /// Copy with method for immutable updates
  MachineModel copyWith({
    String? id,
    int? blockNumber,
    MachineStatus? status,
    List<StatusHistoryEntry>? statusHistory,
    String? estimatedFinishTime,
    TelegramMessage? telegramMessage,
  }) {
    return MachineModel(
      id: id ?? this.id,
      blockNumber: blockNumber ?? this.blockNumber,
      status: status ?? this.status,
      statusHistory: statusHistory ?? this.statusHistory,
      estimatedFinishTime: estimatedFinishTime ?? this.estimatedFinishTime,
      telegramMessage: telegramMessage ?? this.telegramMessage,
    );
  }
}
