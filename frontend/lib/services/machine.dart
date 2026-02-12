import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/machine.dart';

/// Service class for handling machine-related API calls
class MachineService {
  final String baseUrl;
  final http.Client? client;

  MachineService({this.baseUrl = 'http://localhost:8000/api', this.client});

  http.Client get _client => client ?? http.Client();

  /// Get all machines
  Future<List<MachineModel>> getAllMachines() async {
    try {
      final response = await _client.get(
        Uri.parse('$baseUrl/machines'),
        headers: {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        final List<dynamic> data = json.decode(response.body);
        return data.map((json) => MachineModel.fromJson(json)).toList();
      } else {
        throw Exception('Failed to load machines: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error fetching machines: $e');
    }
  }

  /// Get a specific machine by ID
  Future<MachineModel> getMachine(String machineId) async {
    try {
      final response = await _client.get(
        Uri.parse('$baseUrl/machines/$machineId'),
        headers: {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        return MachineModel.fromJson(json.decode(response.body));
      } else if (response.statusCode == 404) {
        throw Exception('Machine $machineId not found');
      } else {
        throw Exception('Failed to load machine: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error fetching machine: $e');
    }
  }

  /// Create a new machine
  Future<MachineModel> createMachine(MachineModel machine) async {
    try {
      final response = await _client.post(
        Uri.parse('$baseUrl/machines'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode(machine.toJson()),
      );

      if (response.statusCode == 201) {
        return MachineModel.fromJson(json.decode(response.body));
      } else {
        throw Exception('Failed to create machine: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error creating machine: $e');
    }
  }

  /// Update machine status
  Future<MachineModel> updateMachineStatus({
    required String machineId,
    required MachineStatus status,
    required String user,
    String? estimatedFinishTime,
  }) async {
    try {
      final response = await _client.put(
        Uri.parse('$baseUrl/machines/$machineId/status'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({
          'status': status.toString().split('.').last,
          'user': user,
          'estimated_finish_time': estimatedFinishTime,
        }),
      );

      if (response.statusCode == 200) {
        return MachineModel.fromJson(json.decode(response.body));
      } else if (response.statusCode == 404) {
        throw Exception('Machine $machineId not found');
      } else {
        throw Exception('Failed to update machine: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error updating machine status: $e');
    }
  }

  /// Update machine estimated finish time
  Future<MachineModel> updateEstimatedFinishTime({
    required String machineId,
    required String finishTime,
  }) async {
    try {
      final response = await _client.patch(
        Uri.parse('$baseUrl/machines/$machineId/time'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({'estimated_finish_time': finishTime}),
      );

      if (response.statusCode == 200) {
        return MachineModel.fromJson(json.decode(response.body));
      } else if (response.statusCode == 404) {
        throw Exception('Machine $machineId not found');
      } else {
        throw Exception('Failed to update time: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error updating estimated finish time: $e');
    }
  }

  /// Add or update Telegram message for a machine
  Future<MachineModel> updateTelegramMessage({
    required String machineId,
    required String message,
    String? messageUrl,
  }) async {
    try {
      final response = await _client.put(
        Uri.parse('$baseUrl/machines/$machineId/telegram'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({'message': message, 'message_url': messageUrl}),
      );

      if (response.statusCode == 200) {
        return MachineModel.fromJson(json.decode(response.body));
      } else if (response.statusCode == 404) {
        throw Exception('Machine $machineId not found');
      } else {
        throw Exception(
          'Failed to update telegram message: ${response.statusCode}',
        );
      }
    } catch (e) {
      throw Exception('Error updating telegram message: $e');
    }
  }

  /// Delete a machine
  Future<void> deleteMachine(String machineId) async {
    try {
      final response = await _client.delete(
        Uri.parse('$baseUrl/machines/$machineId'),
        headers: {'Content-Type': 'application/json'},
      );

      if (response.statusCode != 204 && response.statusCode != 200) {
        throw Exception('Failed to delete machine: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error deleting machine: $e');
    }
  }

  /// Get machines by status
  Future<List<MachineModel>> getMachinesByStatus(MachineStatus status) async {
    try {
      final statusStr = status.toString().split('.').last;
      final response = await _client.get(
        Uri.parse('$baseUrl/machines?status=$statusStr'),
        headers: {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        final List<dynamic> data = json.decode(response.body);
        return data.map((json) => MachineModel.fromJson(json)).toList();
      } else {
        throw Exception('Failed to load machines: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error fetching machines by status: $e');
    }
  }

  /// Get machines by type (washer/dryer)
  Future<List<MachineModel>> getMachinesByType(MachineType type) async {
    try {
      final typeStr = type.toString().split('.').last;
      final response = await _client.get(
        Uri.parse('$baseUrl/machines?type=$typeStr'),
        headers: {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        final List<dynamic> data = json.decode(response.body);
        return data.map((json) => MachineModel.fromJson(json)).toList();
      } else {
        throw Exception('Failed to load machines: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error fetching machines by type: $e');
    }
  }

  /// Get machines by block number (55, 57, or 59)
  Future<List<MachineModel>> getMachinesByBlock(int blockNumber) async {
    try {
      final response = await _client.get(
        Uri.parse('$baseUrl/machines?block=$blockNumber'),
        headers: {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        final List<dynamic> data = json.decode(response.body);
        return data.map((json) => MachineModel.fromJson(json)).toList();
      } else {
        throw Exception('Failed to load machines: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error fetching machines by block: $e');
    }
  }

  /// Get machine status history
  Future<List<StatusHistoryEntry>> getMachineHistory(String machineId) async {
    try {
      final response = await _client.get(
        Uri.parse('$baseUrl/machines/$machineId/history'),
        headers: {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        final List<dynamic> data = json.decode(response.body);
        return data.map((json) => StatusHistoryEntry.fromJson(json)).toList();
      } else if (response.statusCode == 404) {
        throw Exception('Machine $machineId not found');
      } else {
        throw Exception('Failed to load history: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error fetching machine history: $e');
    }
  }

  /// Initialize default machines (useful for setup)
  Future<List<MachineModel>> initializeDefaultMachines() async {
    try {
      final response = await _client.post(
        Uri.parse('$baseUrl/machines/initialize'),
        headers: {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 201 || response.statusCode == 200) {
        final List<dynamic> data = json.decode(response.body);
        return data.map((json) => MachineModel.fromJson(json)).toList();
      } else {
        throw Exception(
          'Failed to initialize machines: ${response.statusCode}',
        );
      }
    } catch (e) {
      throw Exception('Error initializing machines: $e');
    }
  }

  /// Dispose of the HTTP client
  void dispose() {
    if (client == null) {
      _client.close();
    }
  }
}
