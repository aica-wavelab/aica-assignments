import { Dataset } from "@marcellejs/core";

// Define a type (enum) for dataset types
export type Task = "miniMASK" | "miniROAD" | "miniTRASH" | "miniRETINA" | "miniSKIN" | "miniMUSEUM";

export async function addInstancesToDataset(fileName : string, dataset : Dataset): Promise<any> {
    const response = await fetch(`${fileName}`);
    if (!response.ok) {
      throw new Error(`Failed to fetch local JSON file: ${fileName}`);
    }
    const jsonData = await response.json();
    
    if (jsonData.marcelleMeta.type === "dataset") {
      // Loop over instances
      for (const instance of jsonData.instances) {
        dataset.create(instance)
      }
    } else {
      console.error("The json file is not a Marcelle dataset");
    }
    return jsonData;
  }

export async function loadDataset(fileName : string, dataset : Dataset) : Promise<any> {
  // Catch errors if non existing file
  try {
    return await addInstancesToDataset(fileName, dataset);
  } catch (error) {
    console.error(error);
  }
};

export async function loadTask(task : Task, trainingSet : Dataset, testSet : Dataset) {
  // Load training and test set
  trainingSet.clear();
  testSet.clear();
  // Await for the dataset to be cleared and the datasetBrowser to be updated
  await new Promise((resolve) => setTimeout(resolve, 800));
  try {
    await loadDataset(`/assets/${task}/${task}_train.json`, trainingSet);
  } catch (error) {
    console.error(error);
  }
  try {
    await loadDataset(`/assets/${task}/${task}_test.json`, testSet);
  } catch (error) {
    console.error(error);
  }
}