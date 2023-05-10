import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:intl/intl.dart';

class DatePickerFormField extends StatefulWidget {
  final String labelText;
  final TextEditingController controller;

  const DatePickerFormField({
    Key? key,
    required this.labelText,
    required this.controller,
  }) : super(key: key);

  @override
  State<DatePickerFormField> createState() => _DatePickerFormFieldState();
}

class _DatePickerFormFieldState extends State<DatePickerFormField> {
  DateTime? _selectedDate;

  void _updateController() {
    if (_selectedDate != null) {
      widget.controller.text = DateFormat('yyyy-MM-dd').format(_selectedDate!);
    } else {
      widget.controller.text = '';
    }
  }

  // the onselect that will be called on tapping datepicker
  Future<void> _selectDate() async {
    final DateTime? picked = await showCupertinoModalPopup<DateTime>(
      context: context,
      builder: (BuildContext context) {
        return CupertinoActionSheet(
          title: const Text('Select a D.O.B'),
          //message: const Text('Please select a date'),
          actions: <Widget>[
            SizedBox(
              height: 200,
              child: CupertinoDatePicker(
                mode: CupertinoDatePickerMode.date,
                initialDateTime: DateTime.now(),
                onDateTimeChanged: (DateTime dateTime) {
                  setState(() {
                    _selectedDate = dateTime;
                  });
                },
              ),
            ),
          ],
          cancelButton: CupertinoButton(
            child: const Text('Select'),
            onPressed: () {
              Navigator.of(context).pop();
            },
          ),
        );
      },
    );

    if (picked != null && picked != _selectedDate) {
      setState(() {
        _selectedDate = picked;
      });
    }
    _updateController();
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 16.0),
      child: SizedBox(
        width: 130.0,
        child: TextFormField(
          controller: widget.controller,
          decoration: InputDecoration(
            labelText: widget.labelText,
            suffixIcon: const Icon(Icons.date_range),
          ),
          onTap: () async {
            FocusScope.of(context).requestFocus(FocusNode());
            await _selectDate();
          },
        ),
      ),
    );
  }
}
