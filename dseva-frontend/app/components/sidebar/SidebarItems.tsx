import Link from "next/link";

interface SidebarItemProps {
    title: string;
    link: string;
}
const SidebarItem = ({title, link}: SidebarItemProps)  => {
//const SidebarItem = ()  => {
    return (
            <div className="p-2.5 mt-3 flex items-center rounded-md px-4 duration-300 cursor-pointer hover:bg-blue-600 text-white">
                <i className="bi bi-house-door-fill"></i>
                <span className="text-[15px] ml-4 text-gray-200 font-bold">
                    <Link href={link}>{title}</Link>
                </span>
            </div>
    )
}

export default SidebarItem;