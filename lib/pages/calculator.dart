import 'package:flutter/material.dart';
import 'package:paeds_calculator/components/calculator_input.dart';
import 'package:paeds_calculator/components/tf_cupertino.dart';

import '../components/Buttons.dart';

class CalculatorScreen extends StatelessWidget {
  CalculatorScreen({super.key});

  //text editing controllers

  final heightController = TextEditingController();
  final weightController = TextEditingController();
  final headCircumferenceController = TextEditingController();
  final datepickerform = TextEditingController();

  // sign user in method

  void charts() {}

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.blueGrey[200],
      body: SafeArea(
        child: Center(
          child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
            const SizedBox(height: 5),

            //Logo
            const Icon(
              Icons.calculate,
              size: 100,
              color: Colors.black,
            ),

            const SizedBox(height: 10),

            const Text(
              'Please enter parameters below for percentiles!',
              style: TextStyle(
                color: Colors.blueGrey,
                fontSize: 16,
              ),
            ),

            const SizedBox(height: 5),

            // Date picker
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                DatePickerFormField(
                  controller: datepickerform,
                  labelText: 'D.O.B',
                )
              ],
            ),

            const SizedBox(height: 4),

            // Height
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const Text(
                  'height',
                  style: TextStyle(color: Colors.black),
                ),
                MyTextFIeld(
                  controller: heightController,
                  hintText: 'cm',
                ),
              ],
            ),

            const SizedBox(height: 4),

            //weight
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const Text(
                  'weight',
                  style: TextStyle(color: Colors.black),
                ),
                MyTextFIeld(
                  controller: weightController,
                  hintText: 'kgs',
                ),
              ],
            ),

            const SizedBox(height: 4),

            //headcircumference
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const Text(
                  'H_Circumference',
                  style: TextStyle(color: Colors.black),
                ),
                MyTextFIeld(
                  controller: headCircumferenceController,
                  hintText: 'cm',
                ),
              ],
            ),

            const SizedBox(height: 25),

            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                MyButton(onTap: charts),
              ],
            )
          ]),
        ),
      ),
    );
  }
}
