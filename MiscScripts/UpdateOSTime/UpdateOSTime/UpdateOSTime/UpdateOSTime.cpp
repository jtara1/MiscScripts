// UpdateOSTime.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <windows.h>
#include <iostream>

/* source from: https://stackoverflow.com/a/652391/3854436
 * VS 2017 needed some project config changes: https://stackoverflow.com/a/20595744/3854436
 */
namespace JDanielSmith
{
	class Utilities abstract sealed /* abstract sealed = static */
	{
	public:
		static void SetSystemTime(System::DateTime dateTime) {
			LARGE_INTEGER largeInteger;
			largeInteger.QuadPart = dateTime.ToFileTimeUtc(); // "If your compiler has built-in support for 64-bit integers, use the QuadPart member to store the 64-bit integer."


			FILETIME fileTime; // "...copy the LowPart and HighPart members [of LARGE_INTEGER] into the FILETIME structure."
			fileTime.dwHighDateTime = largeInteger.HighPart;
			fileTime.dwLowDateTime = largeInteger.LowPart;


			SYSTEMTIME systemTime;
			if (FileTimeToSystemTime(&fileTime, &systemTime))
			{
				if (::SetSystemTime(&systemTime))
					return;
			}


			HRESULT hr = HRESULT_FROM_WIN32(GetLastError());
			throw System::Runtime::InteropServices::Marshal::GetExceptionForHR(hr);
		}
	};
}

int main()
{
	JDanielSmith::Utilities::SetSystemTime(System::DateTime::Now);
	std::cout << "System time updated";
	std::cin.ignore();
    return 0;
}

