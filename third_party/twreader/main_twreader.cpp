/*  main_twreader.cpp -- read each record from raw pages stored 
 *				in Tianwang format.
 *
 *  Created: Yan  Hongfei, Peking Univ. <yhf@net.pku.edu.cn>
 *	
 *  Created: April 16 20:42am 2006. version 0.1.1
 *              # This is the main program of a twreader.
 *				# using TWReader & Compress classes written by
 *				# Zhang Minghui
 *
 */

#include "TWReader.h"
#include "Compress.h"

static void dohelp(int argc, char *argv[])
{
	cout << "usage : " << argv[0] << "twPageFile" << endl;
	cout << "twPageFile : 天网格式的网页存储文件." << endl;

	return;
}


int main(int argc, char *argv[])
{
	if (argc != 2)
	{
		dohelp(argc, argv);
		return 1;
	}
		
	try {
		TWReader reader(argv[1]);

		const TWReader::T_PageRecord *record = NULL;
		
		//int i = 0;
        string str;
		while ((record = reader.nextRecord()) != NULL)
		{
			//cout << "version : " << record->version << endl;
			//cout << "id : " << record->id << endl;
			//cout << "url : " << record->url << endl;
			//cout << "date : " << record->date << endl;
			//cout << "ip : " << record->ip << endl;
			//cout << "length : " << record->length << endl;

			//cout << "body : " << endl << record->body << endl;
            str = record->body;
            while ( str.find ("\r\n") != string::npos )
            {
                str.erase ( str.find ("\r\n"), 2 );
            }
            while ( str.find ("\n") != string::npos )
            {
                str.erase ( str.find ("\n"), 1 );
            }
            cout << record->id << "\t" << str << endl;

		}
	} catch (TWReaderException &E) {
		cout << E.what() << endl;
	} catch (exception &E) {
		cout << E.what() << endl;
	}

	return 0;
}
