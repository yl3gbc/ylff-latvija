@extends('ylff.admin.layout')
@section('title', __('ylff_admin.overview').' — '.__('ylff_admin.title'))
@section('sidebar')
<nav class="ylff-admin-menu">
<a class="active" href="/ylff/admin?lang={{ app()->getLocale() }}"><span>▦</span>{{ __('ylff_admin.overview') }}</a>
<a href="#"><span>⇩</span>{{ __('ylff_admin.adif_imports') }}</a>
<a href="#"><span>◉</span>{{ __('ylff_admin.activations') }}</a>
<a href="#"><span>◫</span>{{ __('ylff_admin.expeditions') }}</a>
<a href="/ylff/admin/objects?lang={{ app()->getLocale() }}"><span>◆</span>{{ __('ylff_admin.objects') }}</a>
<a href="#"><span>✓</span>{{ __('ylff_admin.activity_check') }}</a>
<a href="#"><span>★</span>{{ __('ylff_admin.awards') }}</a>
<a href="#"><span>≡</span>{{ __('ylff_admin.content') }}</a>
<a href="#"><span>▧</span>{{ __('ylff_admin.media') }}</a>
<a href="#"><span>⚙</span>{{ __('ylff_admin.settings') }}</a>
<a href="/ylff"><span>↗</span>{{ __('ylff_admin.public_page') }}</a><a href="#"><span>⌖</span>{{ __('ylff_admin.map') }}</a>
</nav>@endsection
@section('content')
<div class="ylff-page-heading"><span>YLFF</span><h1>{{ __('ylff_admin.overview') }}</h1><p>{{ __('ylff_admin.subtitle') }}</p></div>
<div class="ylff-dashboard-grid">
<a class="ylff-card ylff-dashboard-card" href="/ylff/admin/objects?lang={{ app()->getLocale() }}"><span class="ylff-card-icon">◆</span><strong>{{ __('ylff_admin.objects') }}</strong><b>—</b></a>
<article class="ylff-card ylff-dashboard-card"><span class="ylff-card-icon">◉</span><strong>{{ __('ylff_admin.activations') }}</strong><b>—</b></article><article class="ylff-card ylff-dashboard-card"><span class="ylff-card-icon">⇩</span><strong>{{ __('ylff_admin.adif_imports') }}</strong><b>—</b></article>
<article class="ylff-card ylff-dashboard-card"><span class="ylff-card-icon">◫</span><strong>{{ __('ylff_admin.expeditions') }}</strong><b>—</b></article><article class="ylff-card ylff-dashboard-card"><span class="ylff-card-icon">★</span><strong>{{ __('ylff_admin.awards') }}</strong><b>—</b></article>
</div>@endsection
