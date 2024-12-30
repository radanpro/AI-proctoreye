import React from "react";
import { Bell, User } from "lucide-react";

const Header = ({ page }) => {
  return (
    <header className="flex justify-between items-center p-4 border-b bg-sky-50 shadow-md ml-64 rounded-md">
      <div>
        <p className="text-sm text-gray-500">Page / {page}</p>
        <h1 className="text-xl font-bold text-gray-800">{page}</h1>
      </div>

      {/* الجهة اليمنى */}
      <div className="flex items-center space-x-4">
        {/* أيقونة الإشعارات */}
        <div className="relative">
          <Bell className="w-6 h-6 text-gray-600 cursor-pointer" />
          <span className="absolute top-0 right-0 w-2 h-2 bg-red-500 rounded-full"></span>
        </div>

        {/* أيقونة الملف الشخصي */}
        <div className="w-8 h-8 rounded-full bg-gray-300 flex items-center justify-center">
          <User className="w-6 h-6 text-gray-600" />
        </div>
      </div>
    </header>
  );
};

export default Header;
