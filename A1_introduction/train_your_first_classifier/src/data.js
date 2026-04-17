import '@marcellejs/core/dist/marcelle.css';
import { dataStore, dataset, datasetBrowser, mobileNet, imageDisplay,
		button, text
		} from '@marcellejs/core';
import { store } from './common';
import { loadTask } from './utils_datasetLoad';
import { base64ToImageData } from './utils_imageLoad';

// DATA COLLECTION AND FEATURES EXTRACTION

export const trainingSet = dataset('trainingSet', store);
export const trainingSetBrowser = datasetBrowser(trainingSet);
trainingSetBrowser.title = "Training set";

export const featureExtractor = mobileNet();

export const testSet = dataset('testSet', store);
export const testSetBrowser = datasetBrowser(testSet);
testSetBrowser.title = "Test set";

// ----------------------------------------------
// TOY DATASET
// ----------------------------------------------

const toyText = text("");
toyText.title = "Toy datasets";

const b_miniFruit = button("miniFRUIT");
b_miniFruit.title = "Fruit classification";

b_miniFruit.$click.subscribe(() => {
	loadTask("miniFRUIT", trainingSet, testSet);
});

// ----------------------------------------------
// SOCIAL DATASETS
// ----------------------------------------------

const socialText = text("");
socialText.title = "Social datasets";

// Masks

const b_miniMask = button("miniMASK");
b_miniMask.title = "Mask classification";

b_miniMask.$click.subscribe(() => {
	loadTask("miniMASK", trainingSet, testSet);
  });

// Traffic lights

const b_miniRoad = button("miniROAD");
b_miniRoad.title = "Traffic light classification";

b_miniRoad.$click.subscribe(() => {
	loadTask("miniROAD", trainingSet, testSet);
  }
)

// Trash

const b_miniTrash = button("miniTRASH");
b_miniTrash.title = "Trash classification";

b_miniTrash.$click.subscribe(() => {
	loadTask("miniTRASH", trainingSet, testSet);
  });

// ----------------------------------------------
// MEDICAL DATASETS
// ----------------------------------------------

const medicalText = text("");
medicalText.title = "Medical datasets";

// Retina
  
const b_miniRetina = button("miniRETINA");
b_miniRetina.title = "Retina disease classification";

b_miniRetina.$click.subscribe(() => {
	loadTask("miniRETINA", trainingSet, testSet);
  });

// Skin
  
const b_miniSkin = button("miniSKIN");
b_miniSkin.title = "Skin cancer classification";

b_miniSkin.$click.subscribe(() => {
	loadTask("miniSKIN", trainingSet, testSet);
  });

import {Stream} from "@marcellejs/core";
export const $selectionStream = trainingSetBrowser.$selected
	.map(array => ({ source: 'training', id: array.length > 0 ? array[array.length - 1] : undefined }))
	.map(({ _, id }) => id)
	.filter(id => id !== undefined)
	.map(id => trainingSet.get(id)).awaitPromises()
	.map((e) => e.thumbnail)
.merge(testSetBrowser.$selected
	.map(array => ({ source: 'test', id: array.length > 0 ? array[array.length - 1] : undefined }))
	.map(({ _, id }) => id)
	.filter(id => id !== undefined)
	.map(id => testSet.get(id)).awaitPromises()
	.map((e) => e.thumbnail))
.map((e) => base64ToImageData(e))
.awaitPromises();

    //     .map(array => ({ source: 'training', id: array.length > 0 ? array[array.length - 1] : undefined }))
    //     .map(({ _, id }) => id)
    //     .filter(id => id !== undefined)
    //     .map(id => trainingSet.get(id)).awaitPromises()
    //     .map((e) => e.thumbnail)
    // .merge(testSetBrowser.$selected
    //     .map(array => ({ source: 'test', id: array.length > 0 ? array[array.length - 1] : undefined }))
    //     .map(({ _, id }) => id)
    //     .filter(id => id !== undefined)
    //     .map(id => testSet.get(id)).awaitPromises()
    //     .map((e) => e.thumbnail))
    // .map((e) => base64ToImageData(e))
    // .awaitPromises();

export const imageViewer = imageDisplay($selectionStream);
imageViewer.title = "Image selected";

export function setup(dash){
    dash.page("Choose your task and dataset")
        .sidebar(imageViewer)
        .use([b_miniFruit, b_miniMask, b_miniRoad, b_miniTrash, b_miniSkin, b_miniRetina], [trainingSetBrowser, testSetBrowser]);
}
