package Plugins::NonLatinForSBClassic::Plugin;

use strict;
use Slim::Display::Lib::Fonts;

sub initPlugin {
	my $class = shift;

	my $pluginDir = Slim::Utils::PluginManager->dataForPlugin($class)->{basedir};

	eval {
		opendir(my $dh, $pluginDir);
		foreach my $file (grep(/\.ttf$/i,readdir($dh))) {
			Slim::Display::Lib::Fonts::addFont($file);
		}
		closedir($dh);
	};

	Slim::Utils::Log::logError("Failed to register font: $@") if $@;
}

1;