import Image from "next/image";
import TableHeader from "../components/tablelist/TableHeader";
import TableRow from "../components/tablelist/TableRow";
import TableList from "../components/tablelist/TableList";

export default function Home() {
  return (

    <div className="relative overflow-x-auto shadow-md sm:rounded-lg  ">


      <div className="bg-white dark:bg-gray-900 pb-10 pt-3 pl-3">
        {/*  <label for="table-search" class="sr-only">Search</label> */}
        <div className="relative">
         {/*  <div className="absolute inset-y-0 rtl:inset-r-0 start-0 flex items-center ps-3 pointer-events-none">
            <svg className="w-4 h-4 text-gray-500 dark:text-gray-400" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 20">
              <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z" /> 
            </svg>
          </div>*/}
          <input type="text" id="table-search" className="block pt-2 ps-10 text-sm text-gray-900 border border-gray-300 rounded-lg w-80 bg-gray-50 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="Search for items" />
        </div>
      </div>


      <TableList />
       {/* <table className="w-full text-sm text-left rtl:text-right text-gray-500 dark:text-gray-400">
        <thead className="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
          <tr>
            <TableHeader title="Title"/>
          </tr>
        </thead>
        <tbody>
          <TableRow title="Test1"/>
          <TableRow title="Test2"/>
          <TableRow title="Test4"/>
        </tbody>
      </table> */}
    </div> 

  );
}
