//
// Copyright 2020 Google LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//

package com.google.privacy.differentialprivacy.example;

import com.google.privacy.differentialprivacy.BoundedMean;
import java.util.Arrays;
import java.util.ArrayList;
import java.io.File; // Import the File class
import java.io.FileNotFoundException; // Import this class to handle errors
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Scanner;
import java.io.FileInputStream;
import java.io.FileWriter;
import java.util.Date;
import java.util.concurrent.TimeUnit;
import java.lang.Math;

public class Main {
	public static void main(String[] args) {
		ArrayList<Double> d1Data = new ArrayList<Double>();
		ArrayList<Double> d2Data = new ArrayList<Double>();
		ArrayList<Double> dpMeans1 = new ArrayList<Double>();
		ArrayList<Double> dpMeans2 = new ArrayList<Double>();
		ArrayList<Long> timeDuration = new ArrayList<Long>();
		double[] epsilons = { 0.5, 1.0, 1.5, 3, 5 };
		String str = "";

		try {

			File fileD1Data = new File("C:\\Users\\MJ\\Desktop\\differential-privacy-main\\examples\\java\\d1Data.csv");
			Scanner myReader = new Scanner(fileD1Data);
			myReader.next();
			while (myReader.hasNextLine()) {
				String value = myReader.nextLine();
				if (value != "") {
					d1Data.add(Double.parseDouble(value));
				}
			}
			myReader.close();

		} catch (FileNotFoundException e) {
			System.out.println("An error occurred.");
			e.printStackTrace();
		}

		try {
			File fileD2Data = new File("C:\\Users\\MJ\\Desktop\\differential-privacy-main\\examples\\java\\d2Data.csv");
			Scanner myReader = new Scanner(fileD2Data);
			myReader.next();
			while (myReader.hasNextLine()) {
				String value = myReader.nextLine();
				if (value != "") {
					d2Data.add(Double.parseDouble(value));
				}
			}
			myReader.close();
		} catch (FileNotFoundException e) {
			System.out.println("An error occurred.");
			e.printStackTrace();
		}
		for (int t = 0; t < 3; t++) {
			long startTime = System.currentTimeMillis();
				for (int i = 0; i < epsilons.length; i++) {
					for (int n = 0; n < 1000; n++) {
						BoundedMean dpBoundedMean1 = BoundedMean.builder().epsilon(epsilons[i]).lower(0).upper(100)
								.maxPartitionsContributed(1).maxContributionsPerPartition(1).build();
						BoundedMean dpBoundedMean2 = BoundedMean.builder().epsilon(epsilons[i]).lower(0).upper(100)
								.maxPartitionsContributed(1).maxContributionsPerPartition(1).build();
						dpBoundedMean1.addEntries(d1Data);
						dpBoundedMean2.addEntries(d2Data);
						dpMeans1.add(dpBoundedMean1.computeResult());
						dpMeans2.add(dpBoundedMean2.computeResult());
					}
				}
			long endTime = System.currentTimeMillis();
			long diff = Math.abs(startTime - endTime);
			System.out.println(diff/(1000.0*60)+diff/1000.0);
			timeDuration.add(diff);

		}

		try {

			FileWriter writer = new FileWriter("dpMeans1.csv");
			for (int i = 0; i < 5000; i++) {
				if (i == 0 || i == 1000 || i == 2000 || i == 3000 || i == 4000) {

					writer.write("epsilon: " + epsilons[i / 1000] + System.lineSeparator());
				}
				writer.write(dpMeans1.get(i) + System.lineSeparator());
			}
			writer.close();
		} catch (Exception e) {
			e.printStackTrace();
		}

		try {

			FileWriter writer = new FileWriter("dpMeans2.csv");
			for (int i = 0; i < 5000; i++) {
				if (i == 0 || i == 1000 || i == 2000 || i == 3000 || i == 4000) {
					writer.write("epsilon: " + epsilons[i / 1000] + System.lineSeparator());
				}
				writer.write(dpMeans2.get(i) + System.lineSeparator());
			}
			writer.close();
		} catch (Exception e) {
			e.printStackTrace();
		}

		try {

			FileWriter writer = new FileWriter("googlePerformance.csv");
			writer.write("Google Time Performance" + System.lineSeparator());
			for (int i = 0; i < timeDuration.size(); i++) {

				writer.write(timeDuration.get(i) + System.lineSeparator());
			}
			writer.close();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
}
