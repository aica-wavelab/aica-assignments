import '@marcellejs/core/dist/marcelle.css';
import { dashboard, dataStore } from '@marcellejs/core';


export const store = dataStore('localStorage');

export const dash = dashboard({
  title: 'Train your visual classifier',
  author: 'Téo Sanchez',
});

