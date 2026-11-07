<?php
namespace App\Http\Controllers\YLFF\Admin;
use App\Http\Controllers\Controller;
use App\Models\YLFFObject;
use Illuminate\Http\Request;
use Illuminate\View\View;
class ObjectController extends Controller
{
    public function index(Request $request): View
    {
        $language = $request->query('lang', 'lv');
        if (!in_array($language, ['lv', 'ru'], true)) { $language = 'lv'; }
        app()->setLocale($language);
        $search = trim((string) $request->query('search', '')); $like = '%'.$search.'%';
        $query = YLFFObject::query(); if ($search !== '') {
            $query->where(function ($query) use ($like) {
                $query->where('reference', 'ilike', $like)->orWhere('name', 'ilike', $like)->orWhere('locator', 'ilike', $like)->orWhere('status', 'ilike', $like);
            });
        }
        $objects = $query->orderBy('reference')->get();
        return view('ylff.admin.objects', ['objects' => $objects, 'search' => $search]);
    }
}
