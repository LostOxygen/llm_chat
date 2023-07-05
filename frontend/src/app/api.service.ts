import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})

export class ApiService {
  url: string = "https://llmchat.free.beeceptor.com/todos"
  options?: any
  constructor(private http: HttpClient) {

   }

   public get(): Observable<any> {
    return this.http.get(this.url);
   }
}
