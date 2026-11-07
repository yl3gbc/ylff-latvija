<!DOCTYPE html>
<html lang="{{ app()->getLocale() }}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>@yield('title', __('ylff_admin.title'))</title>
<link rel="stylesheet" href="/ylff-admin.css">
</head><body>
<div class="ylff-admin">
<header class="ylff-admin-header">
<a class="ylff-admin-brand" href="/">
<img src="/img/logo-small.png" alt="YLFF">
<span><strong>{{ __('ylff_admin.title') }}</strong><small>{{ __('ylff_admin.subtitle') }}</small></span>
</a>
<nav class="ylff-admin-languages" aria-label="{{ __('ylff_admin.language') }}">
<a href="?lang=lv">LV</a><a href="?lang=ru">RU</a>
</nav>
</header>
<div class="ylff-admin-body">
<aside class="ylff-admin-sidebar">@yield('sidebar')</aside>
<main class="ylff-admin-content">@yield('content')</main>
</div>
</div></body></html>
