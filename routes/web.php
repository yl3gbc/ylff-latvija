<?php

use App\Http\Controllers\YLFF\Admin\ObjectController;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;

Route::get('/ylff', function () {
    return view('welcome');
})->name('ylff.public');

Route::get('/ylff/admin', function (Request $request) {
    $language = $request->query('lang', 'lv');
    if (!in_array($language, ['lv', 'ru'], true)) { $language = 'lv'; }
    app()->setLocale($language);
    return view('ylff.admin.dashboard');
})->name('ylff.admin.dashboard');

Route::get('/ylff/admin/objects', [ObjectController::class, 'index'])
    ->name('ylff.admin.objects');
