package test;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader; //ME
import java.io.IOException; //ME
import java.util.HashSet; //ME
import java.util.Set; //ME
import java.io.FileInputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;

import kale.struct.Matrix;

public class Eval_LinkPrediction {
	public int iNumberOfEntities;
	public int iNumberOfRelations;
	public int iNumberOfFactors;
	
	public Matrix MatrixE = null;
	public Matrix MatrixR = null;
	List<Double> iFiltList = new ArrayList<Double>();
	List<Double> iRawList = new ArrayList<Double>();
	public HashMap<String, Boolean> lstTriples = null;
	
	
	public Eval_LinkPrediction(int iEntities, int iRelations, int iFactors) {
		iNumberOfEntities = iEntities;
		iNumberOfRelations = iRelations;
		iNumberOfFactors = iFactors;
	}
	
	public void LPEvaluation(
			String fnMatrixE, 
			String fnMatrixR, 
			String fnTrainTriples, 
			String fnValidTriples, 
			String fnTestTriples,
                        String sat_file) throws Exception {
		preprocess(fnTrainTriples,fnValidTriples,fnTestTriples,fnMatrixE, fnMatrixR);
		evaluate(fnTestTriples, sat_file);
	}
	
	public void preprocess(
			String fnTrainTriples, String fnValidTriples, String fnTestTriples, 
			String fnMatrixE, String fnMatrixR) throws Exception {
		MatrixE = new Matrix(iNumberOfEntities, iNumberOfFactors);
		MatrixE.load(fnMatrixE);
		
		MatrixR = new Matrix(iNumberOfRelations, iNumberOfFactors);
		MatrixR.load(fnMatrixR);
		
		BufferedReader train = new BufferedReader(new InputStreamReader(
				new FileInputStream(fnTrainTriples), "UTF-8"));	
		BufferedReader valid = new BufferedReader(new InputStreamReader(
				new FileInputStream(fnValidTriples), "UTF-8"));
		BufferedReader test = new BufferedReader(new InputStreamReader(
				new FileInputStream(fnTestTriples), "UTF-8"));
		lstTriples = new HashMap<String, Boolean> ();
		String line = "";
		while ((line = train.readLine()) != null) {
			if (!lstTriples.containsKey(line.trim())) {

					lstTriples.put(line.trim(), true);
				} 
		}	
		line = "";
		while ((line = valid.readLine()) != null) {
			if (!lstTriples.containsKey(line.trim())) {

				lstTriples.put(line.trim(), true);
			} 
		}
		line = "";
		while ((line = test.readLine()) != null) {
			if (!lstTriples.containsKey(line.trim())) {

				lstTriples.put(line.trim(), true);
			} 

		}
		System.out.println("triples:"+lstTriples.size());
		valid.close();
		test.close();
		train.close();
	}
	
	public void evaluate(String fnTestTriples, String sat_file) throws Exception {
		BufferedReader reader = new BufferedReader(new InputStreamReader(
				new FileInputStream(fnTestTriples), "UTF-8"));
		String line = "";
		int iCnt = 0;
		double dTotalMeanRank_filt = 0.0;
		double dTotalMRR_filt = 0.0;
		int iTotalHits1_filt = 0;
		int iTotalHits3_filt = 0;
		int iTotalHits5_filt = 0;
		int iTotalHits10_filt = 0;
		double dMedian_filt = 0.0;
		
		double dTotalMeanRank_raw = 0.0;
		double dTotalMRR_raw = 0.0;
		int iTotalHits1_raw = 0;
		int iTotalHits3_raw = 0;
		int iTotalHits5_raw = 0;
		int iTotalHits10_raw = 0;
		double dMedian_raw = 0.0;

		int new_metric_true = 0; //ME
		int new_metric_contradict = 0; //ME
		int new_metric_not_found = 0; //ME

		
		while ((line = reader.readLine()) != null) {
			//System.out.println("triple:" + iCnt/2);
			String[] tokens = line.split("\t");
			int iRelationID = Integer.parseInt(tokens[1]);
			int iSubjectID = Integer.parseInt(tokens[0]);
			int iObjectID = Integer.parseInt(tokens[2]);
			double dTargetValue = 0.0;
			for (int p = 0; p < iNumberOfFactors; p++) {
				dTargetValue -= Math.abs(MatrixE.get(iSubjectID, p) + MatrixR.get(iRelationID, p) - MatrixE.get(iObjectID, p));
			}
			
			int iLeftRank_filt = 1;
			int iLeftIdentical_filt = 0;
			int iLeftRank_raw = 1;
			int iLeftIdentical_raw = 0;
			
			double max_dValue = dTargetValue; //ME
			int max_dValue_ID = iSubjectID; //ME

			for (int iLeftID = 0; iLeftID < iNumberOfEntities; iLeftID++) {
				double dValue = 0.0;
				String negTiple = iLeftID + "\t" + iRelationID + "\t" +iObjectID;
				for (int p = 0; p < iNumberOfFactors; p++) {
					dValue -= Math.abs(MatrixE.get(iLeftID, p) + MatrixR.get(iRelationID, p) - MatrixE.get(iObjectID, p));
				}
				if(!lstTriples.containsKey(negTiple)){
					if (dValue > dTargetValue) {
						iLeftRank_filt++;
                                                if (dValue > max_dValue) {
							max_dValue = dValue; //ME
							max_dValue_ID = iLeftID; //ME
                                                }
					}
					if (dValue == dTargetValue) {
						iLeftIdentical_filt++;
					}
				}	
				if (dValue > dTargetValue) {
					iLeftRank_raw++;
				}
				if (dValue == dTargetValue) {
					iLeftIdentical_raw++;
				}
			}

			//This following part if form ME
			if (new File(sat_file).exists()) {
				boolean foundFirst = false;
				boolean foundSecond = false;

				BufferedReader br = new BufferedReader(new FileReader(sat_file));
				String line_me;

				while ((line_me = br.readLine()) != null) {
					String[] parts = line_me.split("\\s+"); // Split by whitespace

					// Check if the line has at least 3 parts
						if (parts.length >= 3) {
						String subjectId = parts[0];
						String relationID = parts[1];
						String objectID = parts[2];

						// Check for the first condition
						if (subjectId.equals(String.valueOf(iSubjectID)) && objectID.equals(String.valueOf(iObjectID))) {
							foundFirst = true;
						}

						// Check for the second condition
						if (subjectId.equals(String.valueOf(max_dValue_ID)) && relationID.equals(String.valueOf(iRelationID)) && objectID.equals(String.valueOf(iObjectID))) {
							foundSecond = true;
						}
					}
				}

				// Print results based on the flags
				if (foundFirst && !foundSecond) {
					new_metric_contradict = new_metric_contradict + 1;
				} else if (foundFirst && foundSecond) {
					new_metric_true = new_metric_true + 1;
				} else {
					new_metric_not_found = new_metric_not_found + 1;
				}
			} 

			//End of the part form ME



			double dLeftRank_filt = (double)iLeftRank_filt;
			double dLeftRank_raw = (double)(2.0 * iLeftRank_raw + iLeftIdentical_raw -1.0) / 2.0;
			int iLeftHitsAt1_filt = 0,iLeftHitsAt3_filt = 0,iLeftHitsAt5_filt = 0,iLeftHitsAt10_filt = 0;
			int iLeftHitsAt1_raw = 0,iLeftHitsAt3_raw = 0,iLeftHitsAt5_raw = 0,iLeftHitsAt10_raw = 0;
			if (dLeftRank_filt <= 1.0) {
				iLeftHitsAt1_filt = 1;
			}
			if (dLeftRank_filt <= 3.0) {
				iLeftHitsAt3_filt = 1;
			}
			if (dLeftRank_filt <= 5.0) {
				iLeftHitsAt5_filt = 1;
			}
			if (dLeftRank_filt <= 10.0) {
				iLeftHitsAt10_filt = 1;
			}
			
			if (dLeftRank_raw <= 1.0) {
				iLeftHitsAt1_raw = 1;
			}
			if (dLeftRank_raw <= 3.0) {
				iLeftHitsAt3_raw = 1;
			}
			if (dLeftRank_raw <= 5.0) {
				iLeftHitsAt5_raw = 1;
			}
			if (dLeftRank_raw <= 10.0) {
				iLeftHitsAt10_raw = 1;
			}
		
			dTotalMeanRank_filt += dLeftRank_filt;
			dTotalMRR_filt += 1.0/(double)dLeftRank_filt;
			iTotalHits1_filt += iLeftHitsAt1_filt;
			iTotalHits3_filt += iLeftHitsAt3_filt;
			iTotalHits5_filt += iLeftHitsAt5_filt;
			iTotalHits10_filt += iLeftHitsAt10_filt;
			iFiltList.add(dLeftRank_filt);
			
			dTotalMeanRank_raw += dLeftRank_raw;
			dTotalMRR_raw += 1.0/(double)dLeftRank_raw;
			iTotalHits1_raw += iLeftHitsAt1_raw;
			iTotalHits3_raw += iLeftHitsAt3_raw;
			iTotalHits5_raw += iLeftHitsAt5_raw;
			iTotalHits10_raw += iLeftHitsAt10_raw;
			iRawList.add(dLeftRank_raw);
			iCnt++;
			
			int iRightRank_filt = 1;
			int iRightIdentical_filt = 0;
			int iRightRank_raw = 1;
			int iRightIdentical_raw = 0;
			double max_dValue2 = dTargetValue; //ME
			int max_dValue_ID2 = iObjectID; //ME
			for (int iRightID = 0; iRightID < iNumberOfEntities; iRightID++) {
				double dValue = 0.0;
				String negTiple = iSubjectID + "\t" + iRelationID + "\t" +iRightID;
				for (int p = 0; p < iNumberOfFactors; p++) {
					dValue -= Math.abs(MatrixE.get(iSubjectID, p) + MatrixR.get(iRelationID, p) - MatrixE.get(iRightID, p));
				}
				if(!lstTriples.containsKey(negTiple)){
					if (dValue > dTargetValue) {
						iRightRank_filt++;
                                                if (dValue > max_dValue) {
							max_dValue2 = dValue; //ME
                                                        max_dValue_ID2 = iRightID; //ME
                                                }
					}
					if (dValue == dTargetValue) {
						iRightIdentical_filt++;
					}
				}
				if (dValue > dTargetValue) {
					iRightRank_raw++;
				}
				if (dValue == dTargetValue) {
					iRightIdentical_raw++;
				}	
			}

			//This following part is form ME
			if (new File(sat_file).exists()) {
				boolean foundFirst = false;
				boolean foundSecond = false;

				BufferedReader br2 = new BufferedReader(new FileReader(sat_file));
				String line_me;

				while ((line_me = br2.readLine()) != null) {
					String[] parts2 = line_me.split("\\s+"); // Split by whitespace

					// Check if the line has at least 3 parts2
					if (parts2.length >= 3) {

						String subjectId2 = parts2[0];
						String relationID2 = parts2[1];
						String objectID2 = parts2[2];

						// Check for the first condition
						if (subjectId2.equals(String.valueOf(iSubjectID)) && objectID2.equals(String.valueOf(iObjectID))) {
							foundFirst = true;
						}

						// Check for the second condition
						if (subjectId2.equals(String.valueOf(iSubjectID)) && relationID2.equals(String.valueOf(iRelationID)) && objectID2.equals(String.valueOf(max_dValue_ID2))) {
							foundSecond = true;
						}
					}
				}

				// Print results based on the flags
				if (foundFirst && !foundSecond) {
					new_metric_contradict = new_metric_contradict + 1;
				} else if (foundFirst && foundSecond) {
					new_metric_true = new_metric_true + 1;
				} else {
					new_metric_not_found = new_metric_not_found + 1;
				}
			}

            //End of the part form ME
			
			double dRightRank_filt = (double)iRightRank_filt;
			double dRightRank_raw = (double)(2.0 * iRightRank_raw + iRightIdentical_raw -1.0) / 2.0;
			int iRightHitsAt1_filt = 0,iRightHitsAt3_filt = 0,iRightHitsAt5_filt = 0,iRightHitsAt10_filt = 0;
			int iRightHitsAt1_raw = 0,iRightHitsAt3_raw = 0,iRightHitsAt5_raw= 0,iRightHitsAt10_raw = 0;
			if (dRightRank_filt <= 1.0) {
				iRightHitsAt1_filt = 1;
			}
			if (dRightRank_filt <= 3.0) {
				iRightHitsAt3_filt = 1;
			}
			if (dRightRank_filt <= 5.0) {
				iRightHitsAt5_filt = 1;
			}
			if (dRightRank_filt <= 10.0) {
				iRightHitsAt10_filt = 1;
			}
			
			if (dRightRank_raw <= 1.0) {
				iRightHitsAt1_raw = 1;
			}
			if (dRightRank_raw <= 3.0) {
				iRightHitsAt3_raw = 1;
			}
			if (dRightRank_raw <= 5.0) {
				iRightHitsAt5_raw = 1;
			}
			if (dRightRank_raw <= 10.0) {
				iRightHitsAt10_raw = 1;
			}
			
			dTotalMeanRank_filt += dRightRank_filt;
			dTotalMRR_filt += 1.0/(double)dRightRank_filt;
			iTotalHits1_filt += iRightHitsAt1_filt;
			iTotalHits3_filt += iRightHitsAt3_filt;
			iTotalHits5_filt += iRightHitsAt5_filt;
			iTotalHits10_filt += iRightHitsAt10_filt;
			iFiltList.add(dRightRank_filt);
			
			dTotalMeanRank_raw += dRightRank_raw;
			dTotalMRR_raw += 1.0/(double)dRightRank_raw;
			iTotalHits1_raw += iRightHitsAt1_raw;
			iTotalHits3_raw += iRightHitsAt3_raw;
			iTotalHits5_raw += iRightHitsAt5_raw;
			iTotalHits10_raw += iRightHitsAt10_raw;
			iRawList.add(dRightRank_raw);
			iCnt++;	
			
		}
		Collections.sort(iFiltList);
		int indx=iFiltList.size()/2;
		if (iFiltList.size()%2==0) {
			dMedian_filt = (iFiltList.get(indx-1)+iFiltList.get(indx))/2.0;
		}
		else {
			dMedian_filt = iFiltList.get(indx);
		}
		
		Collections.sort(iRawList);
		indx=iRawList.size()/2;
		if (iRawList.size()%2==0) {
			dMedian_raw = (iRawList.get(indx-1)+iRawList.get(indx))/2.0;
		}
		else {
			dMedian_raw = iRawList.get(indx);
		}
		
		System.out.println("Filt setting:");
		System.out.println("MeanRank: "+(dTotalMeanRank_filt / (double)iCnt) + "\n"  
				+ "MRR: "+(dTotalMRR_filt / (double)iCnt) + "\n" 
				+ "Median: " + dMedian_filt + "\n" 
				+ "Hit@1: "+((double)iTotalHits1_filt / (double)iCnt) + "\n" 
				+ "Hit@3: " + ((double)iTotalHits3_filt / (double)iCnt) + "\n" 
				+ "Hit@5: " +((double)iTotalHits5_filt / (double)iCnt)+ "\n"
				+ "Hit@10: " +((double)iTotalHits10_filt / (double)iCnt)+ "\n");
		
		System.out.println("Raw setting:");
		System.out.println("MeanRank: "+(dTotalMeanRank_raw / (double)iCnt) + "\n"  
				+ "MRR: "+(dTotalMRR_raw / (double)iCnt) + "\n" 
				+ "Median: " + dMedian_raw + "\n" 
				+ "Hit@1: "+((double)iTotalHits1_raw / (double)iCnt) + "\n" 
				+ "Hit@3: " + ((double)iTotalHits3_raw / (double)iCnt) + "\n" 
				+ "Hit@5: " +((double)iTotalHits5_raw / (double)iCnt)+ "\n"
				+ "Hit@10: " +((double)iTotalHits10_raw / (double)iCnt)+ "\n");
		if (new File(sat_file).exists()) {
			System.out.println("new metric TRUE: "+ new_metric_true + "\n"  
					+ "new metric NOT FOUND: "+ new_metric_not_found + "\n" 
					+ "new metric CONTRADICTION: " + new_metric_contradict + "\n" );
		} else {
			System.out.println("the saturated file: '"+ sat_file + "' does not exist\n");
		}
		

		reader.close();
	}
	
	public static void main(String[] args) throws Exception {

		int iEntities = Integer.parseInt(args[0]);
		int iRelations = Integer.parseInt(args[1]);
		int iFactors = Integer.parseInt(args[2]);
		String fnMatrixE = args[3];
		String fnMatrixR = args[4];
		String fnTrainTriples = args[5];
		String fnValidTriples = args[6];
		String fnTestTriples = args[7];
		String sat_file = args[8];


		
		Eval_LinkPrediction eval = new Eval_LinkPrediction(iEntities, iRelations, iFactors);
		eval.LPEvaluation(fnMatrixE, fnMatrixR, 
				fnTrainTriples, fnValidTriples, fnTestTriples, sat_file);
	}
}
