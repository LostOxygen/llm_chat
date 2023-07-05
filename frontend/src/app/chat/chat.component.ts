import { Component } from '@angular/core';
import { ApiService } from '../api.service';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-chat',
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.scss']
})

export class ChatComponent {
    messages: any[] = [];
    constructor(private api: ApiService) { 
        this.api.get().subscribe((data: any[])=>{  
            console.log(data);  
            this.messages = data;  
        })
    }
}
