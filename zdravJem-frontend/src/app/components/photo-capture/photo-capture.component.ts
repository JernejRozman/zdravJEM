import { Component } from '@angular/core';

@Component({
  selector: 'app-photo-capture',
  standalone: false,
  templateUrl: './photo-capture.component.html',
  styleUrls: ['./photo-capture.component.css']
})
export class PhotoCaptureComponent {
  uploading = false;
  uploadComplete = false;

  handlePhoto(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      const file = input.files[0];
      console.log('Fake upload started for:', file.name);

      this.uploading = true;
      this.uploadComplete = false;

      setTimeout(() => {
        this.uploading = false;
        this.uploadComplete = true;

        setTimeout(() => {
          this.uploadComplete = false;
        }, 2000);
      }, 2000);
    }
  }
}
