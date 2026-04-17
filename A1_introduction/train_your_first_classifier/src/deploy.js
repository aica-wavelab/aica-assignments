import '@marcellejs/core/dist/marcelle.css';
import { confidencePlot, imageUpload, imageDisplay } from '@marcellejs/core';
import { featureExtractor, trainingSetBrowser, testSetBrowser, $selectionStream} from './data';
import { classifierMLP } from './training';

const newImageSource = imageUpload();
newImageSource.title = "Upload new image to be classified";

const $predictionStream = $selectionStream.merge(newImageSource.$images)
  .filter(() => classifierMLP.ready)
  .map(async (img) => classifierMLP.predict(await featureExtractor.process(img)))
  .awaitPromises();

const deployImageViewer = imageDisplay($selectionStream.merge(newImageSource.$images));
deployImageViewer.title = "Image selected";


const plotResults = confidencePlot($predictionStream);
plotResults.title = "Prediction confidence";


export function setup(dash){
    dash.page("Deployment")
        .sidebar(deployImageViewer, plotResults)
        .use([trainingSetBrowser, testSetBrowser], newImageSource );
}
