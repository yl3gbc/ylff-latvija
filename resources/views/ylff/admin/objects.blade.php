@extends('ylff.admin.layout')
@section('title', __('ylff_admin.objects').' — '.__('ylff_admin.title'))
@section('sidebar')
<nav class="ylff-admin-menu">
<a href="/ylff/admin?lang={{ app()->getLocale() }}"><span>▦</span>{{ __('ylff_admin.overview') }}</a><a href="#"><span>⇩</span>{{ __('ylff_admin.adif_imports') }}</a>
<a href="#"><span>◉</span>{{ __('ylff_admin.activations') }}</a><a href="#"><span>◫</span>{{ __('ylff_admin.expeditions') }}</a>
<a class="active" href="/ylff/admin/objects?lang={{ app()->getLocale() }}"><span>◆</span>{{ __('ylff_admin.objects') }}</a>
<a href="#"><span>✓</span>{{ __('ylff_admin.activity_check') }}</a><a href="#"><span>★</span>{{ __('ylff_admin.awards') }}</a>
<a href="#"><span>≡</span>{{ __('ylff_admin.content') }}</a><a href="#"><span>▧</span>{{ __('ylff_admin.media') }}</a>
<a href="#"><span>⚙</span>{{ __('ylff_admin.settings') }}</a><a href="/ylff"><span>↗</span>{{ __('ylff_admin.public_page') }}</a><a href="#"><span>⌖</span>{{ __('ylff_admin.map') }}</a>
</nav>@endsection
@section('content')
<div class="ylff-page-heading"><span>YLFF</span><h1>{{ __('ylff_admin.objects') }}</h1><p>{{ __('ylff_admin.objects_description') }}</p></div>
<form class="ylff-admin-toolbar" method="GET" action="/ylff/admin/objects"><input type="hidden" name="lang" value="{{ app()->getLocale() }}">
<label><span>⌕</span><input name="search" type="search" value="{{ $search }}" placeholder="{{ __('ylff_admin.search_objects') }}"></label>
<div><button type="submit" title="{{ __('ylff_admin.search_objects') }}">⌕</button><button type="button">＋ {{ __('ylff_admin.add_object') }}</button></div></form>
<div class="ylff-table-wrap"><table class="ylff-admin-table"><thead><tr><th>{{ __('ylff_admin.reference') }}</th><th>{{ __('ylff_admin.object_name') }}</th><th>{{ __('ylff_admin.locator') }}</th><th>{{ __('ylff_admin.latitude') }}</th><th>{{ __('ylff_admin.longitude') }}</th><th>{{ __('ylff_admin.status') }}</th><th>{{ __('ylff_admin.actions') }}</th></tr></thead>
<tbody>@forelse($objects as $object)
<tr><td><strong>{{ $object->reference }}</strong></td><td>{{ $object->name }}</td><td>{{ $object->locator ?: '—' }}</td><td>{{ $object->latitude ?? '—' }}</td><td>{{ $object->longitude ?? '—' }}</td><td>{{ $object->status }}</td><td>—</td></tr>
@empty
<tr><td class="ylff-empty-table" colspan="7">{{ __('ylff_admin.no_objects') }}</td></tr>
@endforelse</tbody>
</table></div>@endsection
