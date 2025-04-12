import { Component } from '@angular/core';

@Component({
  selector: 'app-friends',
  standalone: false,
  templateUrl: './friends.component.html',
  styleUrl: './friends.component.css'
})
export class FriendsComponent {
  cameraInput: any;

  sendRequest(foodieGuy: string) {
    alert(`Friend request sent to ${foodieGuy}`);
  }


  uploading = false;
  uploadComplete = false;

  handlePhoto(event: Event): void {
    const input = event.target as HTMLInputElement;

    if (input.files && input.files.length > 0) {
      const file = input.files[0];
      console.log('Fake uploading:', file);

      this.uploading = true;
      this.uploadComplete = false;

      setTimeout(() => {
        this.uploading = false;
        this.uploadComplete = true;

        setTimeout(() => this.uploadComplete = false, 2000);
      }, 2000);
    }
  }



}
