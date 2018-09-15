import { HttpClientModule, HttpClientXsrfModule } from '@angular/common/http';
import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { BrowserModule } from '@angular/platform-browser';
import { RouterModule } from '@angular/router';

import { TypeaheadModule } from 'ngx-bootstrap';

import {
  AuthService,
  RecipeService
} from './services';
import { LoggedIn } from './guards';
import {
  RecipeDetailResolver,
  RecipeListResolver,
  RecipeReviewResolver,
  UserRecipeListResolver
} from './resolvers';
import {
  AppComponent,
  HomeComponent,
  LogInComponent,
  ProfileComponent,
  RecipeComponent,
  RecipeDetailComponent,
  RecipeListComponent,
  RecipeReviewComponent,
  SignUpComponent,
  UserRecipeListComponent
} from './components';

import { ROUTES } from './app.routes';

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    LogInComponent,
    ProfileComponent,
    RecipeComponent,
    RecipeDetailComponent,
    RecipeListComponent,
    RecipeReviewComponent,
    SignUpComponent,
    UserRecipeListComponent
  ],
  imports: [
    HttpClientModule,
    HttpClientXsrfModule.withOptions({
      cookieName: 'csrftoken',
      headerName: 'X-CSRFToken'
    }),
    FormsModule,
    ReactiveFormsModule,
    BrowserModule,
    RouterModule.forRoot(ROUTES, { useHash: true }),
    TypeaheadModule.forRoot()
  ],
  providers: [
    AuthService,
    LoggedIn,
    RecipeService,
    RecipeDetailResolver,
    RecipeListResolver,
    RecipeReviewResolver,
    UserRecipeListResolver
  ],
  bootstrap: [
    AppComponent
  ]
})
export class AppModule { }
