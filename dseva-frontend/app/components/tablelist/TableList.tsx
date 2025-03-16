'use client';

import apiService from "@/app/services/apiService";
import TableHeader from "./TableHeader";
import TableRow from "./TableRow";
import { useEffect, useState } from "react";

/* interface TableListProps {
    title: string;
}

const TableList = ({title}: TableListProps)  => { */

export type RepositoryType = {
  id: string;
  title: string;
}

const TableList = ()  => {
    const [repositories, setRepositories] = useState<RepositoryType[]>([]);
     const getRepositories  = async() => {
        const url= '/api/repositories';

        const tmpProperties = await apiService.get('/api/repositories');

        setRepositories(tmpProperties.data);

    };

    useEffect(() => {
        getRepositories();
    },[]); 
    return (
        <table className="w-full text-sm text-left rtl:text-right text-gray-500 dark:text-gray-400">
        <thead className="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
          <tr>
            <TableHeader title="Title"/>
          </tr>
        </thead>
        <tbody>
          {repositories.map((repository) => {
              return <TableRow repository={repository} key={repository.id} />
          })};
        </tbody>
      </table>
    )
}

export default TableList;