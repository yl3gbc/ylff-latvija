<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class YLFFObject extends Model
{
    protected $table = 'ylff_objects';
    public $timestamps = false;

    protected $fillable = [
        'reference', 'name', 'latitude', 'longitude',
        'locator', 'description', 'image_url', 'is_active',
        'status', 'included_in_reference', 'included_until',
    ];

    protected function casts(): array
    {
        return ['latitude' => 'float', 'longitude' => 'float',
            'is_active' => 'boolean', 'included_until' => 'date'];
    }
}
