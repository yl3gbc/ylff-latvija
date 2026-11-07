<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration {
    public function up(): void {
        Schema::create('ylff_objects', function (Blueprint $table) {
            $table->increments('id');
            $table->string('reference', 20)->unique();
            $table->string('name', 255);
            $table->double('latitude')->nullable(); $table->double('longitude')->nullable();
            $table->string('locator', 20)->nullable(); $table->text('description')->nullable();
            $table->text('image_url')->nullable(); $table->boolean('is_active')->default(true);
            $table->string('status', 20)->default('active');
            $table->string('included_in_reference', 20)->nullable(); $table->date('included_until')->nullable();
        });
    }
    public function down(): void {
        Schema::dropIfExists('ylff_objects');
    }
};
