package org.seoulai.naivebayes;

import com.sun.deploy.util.StringUtils;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.*;

/**
 * Created by we on 2017. 6. 9..
 */
public class NBclassifier {

    private String[] dataSet;
    private Map<String, Long> classifies = new HashMap<>();
    private Map<String, Map<String, Long>> counter = new HashMap<>();

    public NBclassifier(String[] dataSet) {
        if(dataSet == null || dataSet.length == 0) {
            throw new IllegalArgumentException("Empty dataSet");
        }

        this.dataSet = dataSet;
    }

    private String getClassify(String input) {
        int divide = input.indexOf("|");
        return divide > -1 ? input.substring(0, divide) : null;
    }

    private String[] getWords(String input) {
        int divide = input.indexOf("|");
        return divide > -1 ? input.substring(divide+1).split(",") : null;
    }

    private void training() {
        Arrays.stream(dataSet).forEach(data -> {
            String classify = getClassify(data);
            String[] words = getWords(data);

            if(classify != null){
                Long count = classifies.get(classify);
                if(count == null){
                    count = 1L;
                }else{
                    count++;
                }
                classifies.put(classify, count);

                if(words != null){
                    Arrays.stream(words).forEach(word -> {
                        Map<String, Long> wordCounter = counter.get(classify);
                        if(wordCounter == null) {
                            wordCounter = new HashMap<>();
                            counter.put(classify, wordCounter);
                        }
                        Long wordCount = wordCounter.get(word);
                        if(wordCount == null) {
                            wordCount = 1L;
                        }else{
                            wordCount++;
                        }

                        wordCounter.put(word, wordCount);
                    });
                }
            }
        });
    }

    public String judgement(String[] words) {
        Map<String, Double> results = new HashMap<>();
        long classifiesTotalcount = classifies.values().stream().mapToLong(Long::longValue).sum();
        classifies.forEach((classify, count) -> {
           double[] points = Arrays.stream(words).mapToDouble(word -> {
              Map<String, Long> wordCounter = counter.get(classify);
               if(wordCounter == null) {
                   return 1.0f;
               }
               Long wordCount = wordCounter.get(word);
               if(wordCount == null) {
                   return 1.0f;
               }
               long wordTotalCount = wordCounter.values().stream().mapToLong(Long::longValue).sum();

               return (double) (wordCount + 1) / wordTotalCount;    // smoothing
           }).toArray();

            double total = (double)classifies.get(classify) / classifiesTotalcount;
            total = Arrays.stream(points).reduce(total, (x, y) -> {
                return x * y;
            });
            results.put(classify, total);
        });
        results.entrySet().forEach(entry ->
            System.out.println(String.format("%s : %f", entry.getKey(), entry.getValue())));

        return results.entrySet().stream().max(Map.Entry.comparingByValue(Double::compareTo)).get().getKey();
    }

    public static void main(String[] args) throws IOException {
        // preprocessing
        File hamDir = new File("/Users/we/Downloads/email/ham");
        File spamDir = new File("/Users/we/Downloads/email/spam");

        File[] hamFiles = hamDir.listFiles();
        File[] spamFiles = spamDir.listFiles();

        String[] hamDataSet = getDataSet("ham", hamFiles);
        String[] spamDataSet = getDataSet("spam", spamFiles);

        List<String> trainDataList = new ArrayList<>();
        List<String> testDataList = new ArrayList<>();
        for(int dataSetIdx = 0; dataSetIdx < hamDataSet.length; dataSetIdx++){
            if(dataSetIdx < 18) {
                trainDataList.add(hamDataSet[dataSetIdx]);
                trainDataList.add(spamDataSet[dataSetIdx]);
            }else{
                testDataList.add(hamDataSet[dataSetIdx]);
                testDataList.add(spamDataSet[dataSetIdx]);
            }
        }

        // training data
        String[] dataSet = trainDataList.toArray(new String[trainDataList.size()]);
        for(String s: trainDataList){
            System.out.println(s);
        }

        // training
        NBclassifier classifier = new NBclassifier(dataSet);
        classifier.training();

        // test data
        for(String s : testDataList) {

            String testData = s.split("\\|")[1];
            System.out.println("test data ( " + "label : " + s.split("\\|")[0] + ", data : " + testData+" )");
            String[] words = s.split(",");
            System.out.println("words length : "+words.length);

            String classify = classifier.judgement(words);
            System.out.println(classify);

        }

    }

    private static String[] getDataSet(String label, File[] files) throws IOException {

        List<String> trainData = new ArrayList<>();
        for(File f : files) {
            BufferedReader br = new BufferedReader(new FileReader(f));
            String tmpStr = "";
            List<String> tmpList = new ArrayList<>();
            String line;
            while ((line = br.readLine()) != null) {
                for(String s : line.split("[\\s\\t\\n\\.]")) {
                    String trimedS = s.trim().toLowerCase();
                    if(trimedS == null || "".equals(trimedS) || trimedS.length() == 1)
                        continue;

                    tmpList.add(trimedS);
                }
            }
            trainData.add(label+"|"+ StringUtils.join(tmpList, ","));
        }

        return trainData.toArray(new String[trainData.size()]);
    }

}
