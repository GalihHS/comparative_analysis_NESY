package de.unima.ki.anyburl.threads;

import java.util.ArrayList;
import java.util.HashMap;

import de.unima.ki.anyburl.Settings;
import de.unima.ki.anyburl.algorithm.RuleEngine;
import de.unima.ki.anyburl.data.Triple;
import de.unima.ki.anyburl.data.TripleSet;
import de.unima.ki.anyburl.structure.Rule;

/**
 * The predictor predicts the candidates for a knowledge base completion task.
 * 
 *
 */
public class Predictor extends Thread {
	
	private String path_sat;
	private TripleSet testSet;
	private TripleSet trainingSet;
	private TripleSet validationSet;
	private int k;
	private HashMap<String, ArrayList<Rule>> relation2Rules4Prediction;
	
	
	public Predictor(String path_sat, TripleSet testSet, TripleSet trainingSet, TripleSet validationSet, int k, HashMap<String, ArrayList<Rule>> relation2Rules4Prediction) {
		this.path_sat = path_sat;
		this.testSet = testSet;
		this.trainingSet = trainingSet;
		this.validationSet = validationSet;
		this.k = k;
		this.relation2Rules4Prediction = relation2Rules4Prediction;
	}
	
	
	public void run() {
		int metric_positive = 0;
		int metric_negative = 0;
		int result = 0;
		Triple triple = RuleEngine.getNextPredictionTask();
		// Rule rule = null;
		while (triple != null) {
			// System.out.println(this.getName() + " making prediction for " + triple);
			if (Settings.AGGREGATION_ID == 1) {
				result = RuleEngine.predictMax(path_sat, testSet, trainingSet, validationSet, k, relation2Rules4Prediction, triple);
				metric_positive = metric_positive + result;
				metric_negative = metric_negative + (2 - result);
			}
			triple = RuleEngine.getNextPredictionTask();
		}
		if  (!path_sat.equals("NULL")){
			System.out.println("positive : " + metric_positive + "  -  negative : " + metric_negative);
		}
		
	}

}
