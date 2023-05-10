import 'package:flutter/material.dart';

class MyTextFIeld extends StatelessWidget {
  final dynamic controller;
  final String hintText;

  const MyTextFIeld({
    super.key,
    required this.controller,
    required this.hintText,
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 16.0),
      child: SizedBox(
        width: 120.0,
        child: TextField(
          controller: controller,
          keyboardType: TextInputType.number,
          decoration: InputDecoration(
              enabledBorder: const OutlineInputBorder(
                borderSide: BorderSide(color: Colors.white),
              ),
              focusedBorder: const OutlineInputBorder(
                borderSide: BorderSide(color: Colors.blue),
              ),
              fillColor: Colors.grey,
              filled: true,
              hintText: hintText,
              hintStyle: const TextStyle(color: Colors.white)),
        ),
      ),
    );
  }
}
