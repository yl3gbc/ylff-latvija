<?php
namespace App\Console\Commands;
use App\Models\YLFFObject;
use Illuminate\Console\Attributes\{Description, Signature};
use Illuminate\Console\Command;
use Illuminate\Support\Facades\DB;
#[Signature('app:import-ylff-objects'), Description('Importē YLFF objektus no saglabātā JSON')]
class ImportYlffObjects extends Command
{
    public function handle(): int
    {
        $path = storage_path('app/ylff_objects_import.json');
        if (!is_file($path)) { $this->error('KĻŪDA: importa JSON fails nav atrasts'); return self::FAILURE; }
        if (YLFFObject::query()->exists()) { $this->error('KĻŪDA: ylff_objects tabulā jau ir dati'); return self::FAILURE; }
        $rows = json_decode(file_get_contents($path), true, 512, JSON_THROW_ON_ERROR);
        DB::transaction(function () use ($rows) {
            YLFFObject::query()->insert($rows);
            DB::selectOne("SELECT setval(pg_get_serial_sequence('ylff_objects', 'id'), (SELECT MAX(id) FROM ylff_objects), true)");
        });
        $this->info('OK: importēti '.count($rows).' YLFF objekti');
        return self::SUCCESS;
    }
}
