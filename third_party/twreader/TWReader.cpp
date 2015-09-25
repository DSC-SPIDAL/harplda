/*
 * =====================================================================================
 * 
 *        Filename:  TWReader.cpp
 * 
 *     Description:  
 * 
 *         Version:  1.0
 *         Created:  2005年11月26日 11时38分41秒 CST
 *        Revision:  none
 *        Compiler:  g++
 * 
 *          Author:  张明辉 (), zmh@netera.cn
 *         Company:  天网互联软件研发部
 * 
 * =====================================================================================
 */

#include "TWReader.h"
#include "Compress.h"


TWReader::TWReader()
{
}

TWReader::TWReader(const string &twPageFile) throw (TWReaderException)
{
	mTWFileStream.open(twPageFile.c_str(), ios_base::binary);

	if (!mTWFileStream.is_open())
	{
		string tMsg = "TWReader::TWReader(const string &) open file " + twPageFile 
			+ "error : " + strerror(errno);
		throw TWReaderException(tMsg);
	}
}

TWReader::~TWReader()
{
	if (mTWFileStream.is_open())
		mTWFileStream.close();
}

void TWReader::input(const string &twPageFile) throw (TWReaderException)
{
	if (mTWFileStream.is_open())
		mTWFileStream.close();

	mTWFileStream.open(twPageFile.c_str(), ios_base::binary);

	if (!mTWFileStream.is_open())
	{
		string tMsg = "TWReader::input(const string &) open file " + twPageFile 
			+ "error : " + strerror(errno);
		throw TWReaderException(tMsg);
	}

	return;
}

const TWReader::T_PageRecord *TWReader::nextRecord() throw (TWReaderException)
{
	if (!mTWFileStream.is_open())
	{
		string tMsg = "TWReader::nextRecord() : the TWFileStream is not opened";
		throw TWReaderException(tMsg);
	}

	mPageRecord.clear();
	string tLine;	//!< 行缓冲.

	while (getline(mTWFileStream, tLine))
	{
		if (tLine.find("version: ") != 0)
			continue;
		
		mPageRecord.clear();
		mPageRecord.version = tLine.substr(strlen("version: "));	//!< 取得版本号.
	
        if (getline(mTWFileStream, tLine))	//!< 取得id.
		{
			if (tLine.find("id: ") != 0)
				continue;
			mPageRecord.id = tLine.substr(strlen("id: "));
		} else return NULL;	//!< 文件结束了，还没有读到body, 返回NULL.

	
		if (getline(mTWFileStream, tLine))	//!< 取得url.
		{
			if (tLine.find("url: ") != 0)
				continue;
			mPageRecord.url = tLine.substr(strlen("url: "));
		} else return NULL;	//!< 文件结束了，还没有读到body, 返回NULL.

		if (getline(mTWFileStream, tLine))	//!< 取得date.
		{
			if (tLine.find("date: ") != 0)
				continue;
			mPageRecord.date = tLine.substr(strlen("date: "));
		} else return NULL;

		if (getline(mTWFileStream, tLine))	//!< 取得ip.
		{
			if (tLine.find("ip: ") != 0)
				continue;
			mPageRecord.ip = tLine.substr(strlen("ip: "));
		} else return NULL;


		if (getline(mTWFileStream, tLine))	//!< 取得unzip-length.
		{
			if (tLine.find("unzip-length: ") != 0)
				continue;
			istringstream iss(tLine.substr(strlen("unzip-length: ")).c_str());
			iss >> mPageRecord.unzip_length;
		} else return NULL;
		

		if (getline(mTWFileStream, tLine))	//!< 取得length.
		{
			if (tLine.find("length: ") != 0)
				continue;
			istringstream iss(tLine.substr(strlen("length: ")).c_str());
			iss >> mPageRecord.length;
		} else return NULL;

		if (!getline(mTWFileStream, tLine))	//!< nullLine.
			return NULL;


        //cout << "reading content" << mPageRecord.length << "\n";

        try {
		    //! 开始读取网页内容.
		    char *tBuffer = new char[mPageRecord.length+1];
		    memset(tBuffer, 0, mPageRecord.length+1);
		    mTWFileStream.read(tBuffer, mPageRecord.length);

		    mPageRecord.body = tBuffer;
		    Compress::unCompress(mPageRecord.body, mPageRecord.unzip_length, tBuffer, mPageRecord.length);
		    delete tBuffer;

		    //! 读出一条记录就跳出.
		    break;

	    } catch (CompressException &E) {
	    	cerr << E.what() << endl;
	    } catch (exception &E) {
	    	cerr << E.what() << endl;
	    } catch (...) {
            cerr << "uncatched exception" << endl;
        }
        continue;
	}

	return mPageRecord.version.empty()?NULL:&mPageRecord;
}



#ifdef _TEST

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
		
		int i = 0;

		while ((record = reader.nextRecord()) != NULL)
		{
			cout << "version : " << record->version << endl;
			cout << "id : " << record->id << endl;
			cout << "url : " << record->url << endl;
			cout << "date : " << record->date << endl;
			cout << "ip : " << record->ip << endl;
			cout << "length : " << record->length << endl;

			cout << "body : " << endl << record->body << endl;

			//cout << "sleep 3 seconds ..." << endl;
			//cout << i++ << endl;
			//sleep(3);
		}
	} catch (TWReaderException &E) {
		cout << E.what() << endl;
	//} catch (Exception &E) {
		//cout << E.what() << endl;
	} catch (exception &E) {
		cout << E.what() << endl;
	}

	return 0;
}
#endif //_TEST
