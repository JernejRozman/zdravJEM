import { Component } from '@angular/core';

@Component({
  selector: 'app-tester',
  templateUrl: './tester.component.html',
  styleUrls: ['./tester.component.css']
})
export class TesterComponent {

  constructor() {}

  runTest(): void {
    console.log('🚀 Test action triggered!');
    alert('Test action executed. You can put anything here 🚀');
  }
}
