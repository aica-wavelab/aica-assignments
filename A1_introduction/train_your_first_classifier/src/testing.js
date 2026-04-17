import '@marcellejs/core/dist/marcelle.css';
import { batchPrediction, confusionMatrix, throwError } from '@marcellejs/core';
import { store } from './common';
import { trainingSet, testSet} from './data';
import { classifierMLP } from './training';

const trainingBatchMLP = batchPrediction('mlp', store);
const testBatchMLP = batchPrediction('mlp', store);

const trainingConfMat = confusionMatrix(trainingBatchMLP, trainingSet);
trainingConfMat.title = "Confusion on training set";
const testConfMat = confusionMatrix(testBatchMLP, testSet);
testConfMat.title = "Confusion on test set";


classifierMLP.$training.subscribe(async () => {
        if (!classifierMLP.ready) {
            throwError(new Error('No classifier has been trained'));
          }
        await trainingBatchMLP.clear();
        await testBatchMLP.clear();
        await trainingBatchMLP.predict(classifierMLP, trainingSet);
        await testBatchMLP.predict(classifierMLP, testSet);
    });

export function setup(dash){
    dash.page("Testing")
        .use([trainingConfMat, testConfMat]);
}