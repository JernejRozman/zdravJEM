// test.component.ts
import { Component } from '@angular/core';
import { Firestore, doc, getDoc } from '@angular/fire/firestore';

@Component({
  selector: 'app-test',
  template: `
    <h3>Firestore Test</h3>
    <p>{{ testValue }}</p>
  `,
  standalone: false,
})
export class TestComponent {
  testValue: string = 'No data yet...';

  constructor(private firestore: Firestore) {
    this.checkFirestoreConnection();
  }

  async checkFirestoreConnection() {
    // Create or refer to a doc
    const testDocRef = doc(this.firestore, 'testCollection/myTestDoc');
    // Attempt to get the doc (make sure 'testCollection/myTestDoc' exists in your Firestore!)
    const docSnap = await getDoc(testDocRef);

    if (docSnap.exists()) {
      this.testValue = `Document data: ${JSON.stringify(docSnap.data())}`;
    } else {
      this.testValue = 'No such document!';
    }
  }
}
